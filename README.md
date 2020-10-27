## Expense Entry (Renamed)

ERPNext Expense Entry allows easy capture of non-item expenses without using the Journal Entry,

## Doctype Setup
#### Expense Entry Doctype
```
Users
- Accounts Users - can draft
- Expense Approver - can submit

Doctype Fields - EXP-.YEAR.-#####

- Company
- Request Date (Auto: Read-only Datetime)
- Required Date (Required: Date)
- Payment To

Accounting Dimensions:
- Default Cost Center (Link)
- Default Project (Link)

Section and Table: Expense Details
- Expense Account - (Required: Link - Filtered by Expenses)
- Description - (Data)
- Amount (Required: Currency)
- Cost Center
- Project

Section: Additional Information
- Remarks (Short text)
- Approved By (Read-only)

- column break
- Payment Mode (link)
- Reference
- Reference Date
```

#### Expense Settings (?)
- Expense Approver - Can be done from Accounts settings

## Expense Workflow
1. Pending
2. Approved
3. Rejected
4. Cancelled

## Installation

```bench get-app https://github.com/the-bantoo/expense_request.git
bench --site site-name install-app expense_request```


#### What's Next
This version
- [x] Ask for community input
- [x] Add to Accouting Menus, below JEs
- [] Query Report

Later 
- [ ] Alert Approvers
- [ ] Tax Templates
- [ ] Separate Request Document
- [ ] Rename App. Expense Voucher vs Expense Entry
- [ ] Request addition into ERPNext Core
- [ ] Wrtie tests


#### License

MIT
