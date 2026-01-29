### Ostec Native

To handle additional features

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app ostec_native
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/ostec_native
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

# Renewal Tracking System - User Guide

**Company:** Ostec (Your company & Your company 2)  
**Version:** 1.0  
**Date:** January 29, 2026

---

## Quick Overview

The Renewal Tracking System automatically monitors license expiration dates and alerts you at critical milestones. The system updates itself twice daily - you don't need to do anything manually.

---

## How It Works

### Automatic Updates

- **2:00 AM Daily** - Updates all records
- **2:00 PM Daily** - Updates critical records
- **On Save/Submit** - Calculates stage immediately

### Renewal Stages

| Stage | Days Left | Color | What To Do |
|-------|-----------|-------|------------|
| **Open** | Not started | 🔵 Blue | Wait - license will start automatically |
| **Running** | > 90 days | 🟢 Green | Normal - no action needed |
| **90 Days to Expiry** | 61-90 days | 🟡 Yellow | Contact customer, plan renewal |
| **60 Days to Expiry** | 31-60 days | 🟠 Orange | Send quotation, negotiate |
| **30 Days to Expiry** | 1-30 days | 🔴 Red | URGENT - Daily follow-up |
| **Expired** | 0 or less | 🔴 Red | CRITICAL - Immediate action |

---

## Creating a Renewal Tracking Record

### Step 1: Navigate
Go to: **Ostec Native → Renewal Tracking → New**

### Step 2: Fill Basic Info
- **Renewal Title:** Customer Name - Service Name Renewal
- **Customer:** Select customer
- **Company:** Your company or Your company 2
- **Currency:** GHS (Your company) or CFA (Your company 2)

### Step 3: Enter License Dates (IMPORTANT!)
- **License Start:** When license begins
- **License End:** When license expires

Example:
- License Start: 01-01-2026
- License End: 31-12-2026

### Step 4: Add Items (Optional)
- Click **Add Row**
- Select **Item Code**
- Enter **Qty** and **Rate**
- Amounts calculate automatically

### Step 5: Save & Submit
- Click **Save** - Stage calculates automatically
- Click **Submit** - Now tracked by system

---

## Viewing Records

### List View
**Location:** Ostec Native → Renewal Tracking

**What You See:**
- Customer name
- License dates
- Renewal Stage (color-coded)
- Days Remaining (color-coded)

### Quick Filters
- **Critical:** Filter by "30 Days to Expiry" + "Expired"
- **Upcoming:** Filter by "90 Days" + "60 Days"
- **Active:** Filter by "Running"

---

## Understanding Each Stage

### 🔵 Open (License Not Started)
**Example:** Today is Jan 15, license starts Feb 1
- No action needed
- System will change to "Running" automatically

### 🟢 Running (More than 90 days left)
**Example:** 120 days remaining
- License is healthy
- Monitor periodically

### 🟡 90 Days to Expiry (61-90 days left)
**Example:** 85 days remaining
**Action Plan:**
1. Contact customer this week
2. Discuss renewal needs
3. Prepare quotation
4. Schedule meeting

### 🟠 60 Days to Expiry (31-60 days left)
**Example:** 55 days remaining
**Action Plan:**
1. Send formal quotation
2. Follow up within 3-5 days
3. Negotiate terms
4. Get purchase order

### 🔴 30 Days to Expiry (1-30 days left)
**Example:** 25 days remaining
**URGENT Actions:**
1. Daily customer follow-up
2. Escalate to management
3. Document all communication
4. Prepare for non-renewal

### 🔴 Expired (Past expiry date)
**Example:** -5 days (overdue)
**CRITICAL Actions:**
1. Contact customer immediately
2. Suspend service if applicable
3. Process urgent renewal if approved
4. Create new tracking for renewed period

---

## Multi-Currency Guide

### Your company (GHS)
- Base currency: GHS
- Conversion rate: Always 1.0
- Example: 150 GHS = 150 GHS

### Your company 2 (CFA)
- Base currency: CFA
- Conversion rate: Always 1.0
- Example: 90,000 CFA = 90,000 CFA

### Other Currencies (USD, EUR, etc.)
**If rate exists in system:**
- Select currency
- Rate fills automatically
- Example: 100 USD × 16.5 = 1,650 GHS

**If rate doesn't exist:**
- Select currency
- System asks for rate
- Enter manually
- Example: 200 EUR × 655.957 = 131,191.40 CFA

---

## Common Tasks

### Editing a Draft Document
1. Open document
2. Click **Edit**
3. Make changes
4. Click **Save**
5. Stage recalculates automatically

### Editing a Submitted Document
1. Click **Amend** (can't edit directly)
2. Make changes
3. Save and Submit
4. Creates new version

### Filtering by Stage
1. Click **Filter** icon
2. Select **Renewal Stage**
3. Choose stage(s)
4. Click **Apply**

### Exporting to Excel
1. Apply filters if needed
2. Click **Menu (...)** → **Export**
3. Choose **Excel**
4. Download file

---

## Renewal Process Timeline

### At 90 Days
- Week 1-2: Contact customer
- Week 3-4: Send quotation
- Week 5-6: Follow up
- Week 7+: Finalize terms

### At 60 Days
- Send formal quotation
- Follow up twice weekly
- Negotiate pricing
- Prepare Sales Order

### At 30 Days
- Daily customer contact
- Management escalation
- Document everything
- Prepare backup plan

### At Expiry
- Immediate contact
- Service suspension
- Urgent renewal processing
- Create new tracking if renewed

---

## Best Practices

### ✅ DO
- Use clear, descriptive titles
- Submit documents immediately after creation
- Review 90-day records weekly
- Check 30-day records daily
- Create NEW tracking for renewed periods
- Document all customer communications

### ❌ DON'T
- Leave records in draft status
- Use vague titles like "Renewal 1"
- Wait for customer to contact you
- Let records reach Expired stage
- Modify old records (use Amend instead)
- Delete historical records

---

## Troubleshooting

### Stage Not Updating
**Problem:** Stage shows wrong value
**Solution:**
1. Check if document is submitted
2. Verify license dates are correct
3. Wait for next update (2 AM or 2 PM)
4. Contact System Admin if persistent

### Wrong Currency Conversion
**Problem:** Amount looks incorrect
**Solution:**
1. Verify correct currency selected
2. Check exchange rate value
3. Enter manual rate if needed
4. Recalculate and verify

### Can't Edit Document
**Problem:** Fields are locked
**Reason:** Document is submitted
**Solution:** Click **Amend** button instead of Edit

---

## FAQ

**Q: How often do stages update?**  
A: Automatically at 2 AM and 2 PM daily, plus whenever you save.

**Q: Can I manually change the stage?**  
A: No, it's automatic to prevent errors. Check your dates if stage looks wrong.

**Q: What happens when a license expires?**  
A: Stage changes to "Expired" (red). You must take immediate action.

**Q: Can I delete a renewal record?**  
A: Draft: Yes. Submitted: Use Cancel instead. Keep for audit trail.

**Q: How do I handle a renewed license?**  
A: Create a NEW Renewal Tracking with new dates. Don't modify the old one.

**Q: Why is my days remaining different from my calculation?**  
A: System uses: License End Date - Today's Date. Check dates are correct.

**Q: Can I export data to Excel?**  
A: Yes. Apply filters → Menu (...) → Export → Excel

**Q: How far in advance should I start renewal?**  
A: Start at 90 days. Send quotation at 60 days. Daily follow-up at 30 days.

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│        RENEWAL TRACKING QUICK REFERENCE         │
├─────────────────────────────────────────────────┤
│                                                  │
│  STAGES & ACTIONS:                              │
│  🔵 Open       → Wait for start                 │
│  🟢 Running    → Monitor                        │
│  🟡 90 Days    → Contact customer               │
│  🟠 60 Days    → Send quotation                 │
│  🔴 30 Days    → Daily follow-up                │
│  🔴 Expired    → URGENT action                  │
│                                                  │
│  AUTO-UPDATES:                                  │
│  • 2:00 AM - All records                        │
│  • 2:00 PM - Critical records                   │
│                                                  │
│  NAMING FORMAT:                                 │
│  [Customer] - [Service] - [Year] Renewal       │
│                                                  │
│  CURRENCIES:                                    │
│  • Your company → GHS (rate 1.0)                   │
│  • Your company 2  → CFA (rate 1.0)                   │
│  • Others    → Auto or manual rate              │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Support Contacts

- **System Issues:** IT/System Administrator
- **Process Questions:** Sales Manager
- **Currency/Finance:** Finance Team

---

**End of Guide**

For updates or questions, contact your System Administrator.