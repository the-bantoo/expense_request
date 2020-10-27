from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
	config = [
		
		{
			"label": _("General Ledger"),
			"items": [
				{
					"type": "doctype",
					"name": "Expense Entry",
					"description": _("Capture Expenses"),
            		"link": "List/Expense Entry/Link"
				}
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Expenses Register",
					"doctype": "Expense Entry",
            		"link": "List/Expense Entry/Report/Expenses Register"
					
				}
			]
		}

	]
	return config
