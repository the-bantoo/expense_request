## Expense Request

ERPNext Expense Request

## Doctype Setup
### Expense Request
```
Users
- System/Desk Users - can draft
- Expense Approver - can submit

Doctype Fields - EXP-YEAR-#######
- Request Date (Auto: Read-only Datetime)
- Required Date (Required: Date)

Section and Table: Expense Details
- Expense Account - (Required: Link - Filtered by Expenses)
- Description - (Data)
- Amount (Required: Currency)

Section: Additional Information
- Remarks (Short text)
- column break
- Payment Mode (link)
- Requested by (Data)
```

### Expense Settings (?)
- Expense Approver - Can be done from Accounts settings

## Expense Workflow
1. Draft
2. Submit
3. Approve

## Features
- Create Journal Entry

Installation

`bench get-app https://github.com/the-bantoo/expense_request.git`

`bench --site site-name install-app expense_request`


#### What's Next
- Ask for community input
- Tests
- Request addition into ERPNext Core

#### License

MIT
