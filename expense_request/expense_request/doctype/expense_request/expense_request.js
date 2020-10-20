// Copyright (c) 2020, Bantoo and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Request', {
	onload(frm) {
		frm.set_query("expense_account", 'expense_details', () => {
			return {
				filters: [
					["Account", "parent_account", "Like", "%Indirect Expenses%"]
				]
			}
		});
	}
});
