# Copyright (c) 2026, Richmond Gedziq and contributors
# For license information, please see license.txt

# import frappe
# -*- coding: utf-8 -*-
import json

import frappe
from frappe.model.document import Document
from frappe.utils import flt,getdate,nowdate



class RenewalTracking(Document):
    def validate(self):
        self.set_exchange_rate()
        self.calculate_item_values()
        self.calculate_totals()
    
    def before_save(self):
        self.calculate_item_values()
        self.calculate_totals()
    
    def set_exchange_rate(self):
        """Set exchange rate from Currency Exchange doctype"""
        if not self.currency or not self.company:
            return
        
        company_currency = frappe.db.get_value('Company', self.company, 'default_currency')
        
        # For Ostec Ltd (GHS) or Ostec SA (CFA) - if base currency selected, exchange rate = 1
        if self.currency == company_currency:
            self.exchange_rate = 1.0
            return
        
        # If exchange rate already manually entered, keep it
        if self.exchange_rate and self.exchange_rate > 0:
            return
        
        # Try to find exchange rate from Currency Exchange doctype
        exchange_rate_value = frappe.db.get_value('Currency Exchange',
            {
                'from_currency': self.currency,
                'to_currency': company_currency
            },
            'exchange_rate'
        )
        
        if exchange_rate_value:
            # Found in system, store the exchange rate
            self.exchange_rate = flt(exchange_rate_value)
        else:
            # Currency pair not available in system, user must enter manually
            frappe.throw(
                f'Currency pair {self.currency} to {company_currency} not available in system. '
                'Please enter the exchange rate manually.'
            )
    
    def calculate_item_values(self):
        """Calculate amounts and base currency values for all items"""
        if not self.items:
            return
        
        # Get exchange rate
        exchange_rate = flt(self.exchange_rate) or 1.0
        company_currency = self.get_company_currency()
        
        for item in self.items:
            # Calculate amount = qty * rate
            item.amount = flt(item.qty, 2) * flt(item.rate, 2)
            
            # Calculate base currency values using exchange rate
            if self.currency and company_currency and self.currency != company_currency:
                # Different currencies - apply exchange rate
                item.base_rate = flt(item.rate, 2) * exchange_rate
                item.base_amount = flt(item.amount, 2) * exchange_rate
            else:
                # Same currency (base currency) - no conversion needed
                item.base_rate = item.rate
                item.base_amount = item.amount
    
    def calculate_totals(self):
        """Calculate net_total and net_total_base from all item lines"""
        if not self.items:
            self.net_total = 0.0
            self.net_total_base = 0.0
            return
        
        # Sum all amounts
        self.net_total = sum(flt(item.amount, 2) for item in self.items)
        
        # Sum all base amounts
        self.net_total_base = sum(flt(item.base_amount, 2) for item in self.items)
    
    def get_company_currency(self):
        """Get company's default currency"""
        if self.company:
            return frappe.db.get_value('Company', self.company, 'default_currency')
        return None


@frappe.whitelist()
def import_items(file_url, parent_doc):
    """Import items from uploaded CSV/Excel file"""
    import csv
    import openpyxl
    from frappe.utils.file_manager import get_file_path
    
    # Get the file path
    file_path = get_file_path(file_url)
    
    items = []
    
    try:
        # Determine file type and read accordingly
        if file_url.endswith('.csv'):
            # Read CSV file
            with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get('Item Code'):  # Skip empty rows
                        items.append({
                            'item_code': row.get('Item Code', ''),
                            'item_name': row.get('Item Name', ''),
                            'description': row.get('Description', ''),
                            'brand': row.get('Brand', ''),
                            'item_group': row.get('Item Group', ''),
                            'oum': row.get('UOM', ''),
                            'qty': flt(row.get('Qty', 0)),
                            'rate': flt(row.get('Rate', 0)),
                        })
        else:
            # Read Excel file
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            
            # Get headers from first row
            headers = [cell.value for cell in sheet[1]]
            
            # Read data rows
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0]:  # Skip empty rows (check if Item Code exists)
                    item_data = dict(zip(headers, row))
                    items.append({
                        'item_code': item_data.get('Item Code', ''),
                        'item_name': item_data.get('Item Name', ''),
                        'description': item_data.get('Description', ''),
                        'brand': item_data.get('Brand', ''),
                        'item_group': item_data.get('Item Group', ''),
                        'oum': item_data.get('UOM', ''),
                        'qty': flt(item_data.get('Qty', 0)),
                        'rate': flt(item_data.get('Rate', 0)),
                    })
    except Exception as e:
        frappe.throw(f'Error reading file: {str(e)}')
    
    return items


@frappe.whitelist()
def make_request_for_quotation(source_name, target_doc=None):
    """Create Request for Quotation from Renewal Tracking"""
    from frappe.model.mapper import get_mapped_doc
    
    def set_missing_values(source, target):
        target.transaction_date = frappe.utils.nowdate()
        target.status = "Draft"
    
    def update_item(source, target, source_parent):
        target.schedule_date = frappe.utils.add_days(frappe.utils.nowdate(), 7)
    
    doclist = get_mapped_doc("Renewal Tracking", source_name, {
        "Renewal Tracking": {
            "doctype": "Request for Quotation",
            "field_map": {
                "name": "renewal_tracking",
                "company": "company"
            }
        },
        "Renewal Tracking Item": {
            "doctype": "Request for Quotation Item",
            "field_map": {
                "item_code": "item_code",
                "item_name": "item_name",
                "description": "description",
                "qty": "qty",
                "oum": "uom",
                "brand": "brand"
            },
            "postprocess": update_item
        }
    }, target_doc, set_missing_values)
    
    return doclist


@frappe.whitelist()
def make_supplier_quotation(source_name, target_doc=None):
    """Create Supplier Quotation from Renewal Tracking"""
    from frappe.model.mapper import get_mapped_doc
    
    def set_missing_values(source, target):
        target.transaction_date = frappe.utils.nowdate()
    
    doclist = get_mapped_doc("Renewal Tracking", source_name, {
        "Renewal Tracking": {
            "doctype": "Supplier Quotation",
            "field_map": {
                "name": "renewal_tracking",
                "company": "company",
                "currency": "currency",
                "exchange_rate": "conversion_rate"
            }
        },
        "Renewal Tracking Item": {
            "doctype": "Supplier Quotation Item",
            "field_map": {
                "item_code": "item_code",
                "item_name": "item_name",
                "description": "description",
                "qty": "qty",
                "oum": "uom",
                "rate": "rate",
                "amount": "amount",
                "brand": "brand"
            }
        }
    }, target_doc, set_missing_values)
    
    return doclist


@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
    """Create Customer Quotation from Renewal Tracking"""
    from frappe.model.mapper import get_mapped_doc
    
    def set_missing_values(source, target):
        target.transaction_date = frappe.utils.nowdate()
        target.valid_till = frappe.utils.add_days(frappe.utils.nowdate(), 30)
    
    doclist = get_mapped_doc("Renewal Tracking", source_name, {
        "Renewal Tracking": {
            "doctype": "Quotation",
            "field_map": {
                "name": "renewal_tracking",
                "company": "company",
                "currency": "currency",
                "exchange_rate": "conversion_rate"
            }
        },
        "Renewal Tracking Item": {
            "doctype": "Quotation Item",
            "field_map": {
                "item_code": "item_code",
                "item_name": "item_name",
                "description": "description",
                "qty": "qty",
                "oum": "uom",
                "rate": "rate",
                "amount": "amount",
                "brand": "brand"
            }
        }
    }, target_doc, set_missing_values)
    
    return doclist