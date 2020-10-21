import frappe
from frappe import _
from frappe import utils

"""
Todo
- Print Format - Add signatures
- Creation of JV
  - Workflow: Pending Approval, Approved (set-approved by)
  - Add fixture in accounts settings
  - expense refs
- Settings - Petty Cash / Expenses payment Account
- authorising party

Accounts Settings
Section: Expenses
- Expense Approvers
- Automatically Create Journal Entries



Done
  - Prevent duplicate entry - done
"""
def setup(expense_entry, method):

    # add expenses and set the total field

    total = 0
    for detail in expense_entry.expenses:
        total += float(detail.amount)

    expense_entry.total = total
    make_journal_entry(expense_entry)

@frappe.whitelist()
def initialise_journal_entry(expense_entry_name):
    make_journal_entry(
        frappe.get_doc('Expense Entry', expense_entry_name)
    )


def make_journal_entry(expense_entry):

    # check for duplicates
    
    if frappe.db.exists({'doctype': 'Journal Entry', 'bill_no': expense_entry.name}):
        frappe.throw(
            title="Error",
            msg="Journal Entry {} already exists.".format(expense_entry.name)
        )


    # Preparing the JE: convert expense_entry details into je account details

    accounts = []

    for detail in expense_entry.expenses:
        accounts.append({  
            'debit_in_account_currency': float(detail.amount),
            'user_remark': str(detail.description),
            'account': detail.expense_account,
            'project': expense_entry.project
        })

    # finally add the payment account detail

    pay_account = ""

    if expense_entry.mode_of_payment != "Cash" and (not expense_entry.payment_reference):
        frappe.throw(
            title="Enter Payment Reference",
            msg="Payment Reference is Required for all non-cash payments."
        )

    payment_mode = frappe.get_doc('Mode of Payment', expense_entry.mode_of_payment)
    for acc in payment_mode.accounts:
        pay_account = acc.default_account

    if not pay_account or pay_account == "":
        frappe.throw(
            title="Error",
            msg="The selected Mode of Payment has no linked account."
        )

    accounts.append({  
        'credit_in_account_currency': float(expense_entry.total),
        'user_remark': str(detail.description),
        'account': pay_account
    })

    # create the journal entry
    je = frappe.get_doc({
        'title': expense_entry.name,
        'doctype': 'Journal Entry',
        'voucher_type': 'Journal Entry',
        'posting_date': utils.today(),
        'company': expense_entry.company,
        'accounts': accounts,
        'user_remark': expense_entry.remarks,
        'mode_of_payment': expense_entry.mode_of_payment,
        'cheque_date': expense_entry.clearance_date,
        'cheque_no': expense_entry.payment_reference,
        'pay_to_recd_from': expense_entry.requested_by,
        'bill_no': expense_entry.name
    })

    je.insert()
    je.submit()