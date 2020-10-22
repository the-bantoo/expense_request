import frappe
from frappe import _
from frappe import utils

"""
Todo

Add all the fixtures to the app so that it is fully portable
a. Workflows
b. Accounts Settings Fields

Fix minor issues
a. Approver field vanishing
b. Cant set custom print format as default

Complete functionality
a. Alert Approvers
b. Print Format polish-up - Add signatures
c. Add settings fields to Accounts Settings

Section: Expenses
- Checkbox to Automatically Create Journal Entries
- Settings - Default Expenses Payment Account

Tests


Done
  - Prevent duplicate entry - done
  - Workflow: Pending Approval, Approved (set-approved by)
  - Creation of JV
  - expense refs
  - Roles:
    - Expense Approver
  - Set authorising party
"""
def setup(expense_entry, method):

    # add expenses and set the total field

    total = 0
    count = 0
    for detail in expense_entry.expenses:
        total += float(detail.amount)        
        count += 1

    expense_entry.total = total
    expense_entry.quantity = count

    make_journal_entry(expense_entry)

    


@frappe.whitelist()
def initialise_journal_entry(expense_entry_name):
    # make JE from javascript form Make JE button

    make_journal_entry(
        frappe.get_doc('Expense Entry', expense_entry_name)
    )


def make_journal_entry(expense_entry):

    if expense_entry.status == "Approved":         

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

        if (expense_entry.mode_of_payment != "Cash" and expense_entry.mode_of_payment != "Wire Transfer") and (not expense_entry.payment_reference):
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
            'reference_date': expense_entry.clearance_date,
            'cheque_no': expense_entry.payment_reference,
            'pay_to_recd_from': expense_entry.payment_to,
            'bill_no': expense_entry.name
        })

        user = frappe.get_doc("User", frappe.session.user)

        expense_entry.approved_by = str(user.first_name) + ' ' + str(user.last_name)
        #expense_entry.save()

        je.insert()
        je.submit()