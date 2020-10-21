// Copyright (c) 2020, Bantoo and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Entry', {
	onload(frm) {
		frm.set_query("expense_account", 'expenses', () => {
			return {
				filters: [
					["Account", "parent_account", "Like", "%Indirect Expenses%"]
				]
			}
		});
	},
	refresh: function(frm) {
		frm.add_custom_button(__('Journal Entry'), function(){
			frappe.call({
				method: "expenses.api.initialise_journal_entry",
				args: {
					expense_entry_name: frm.doc.name
				},
				callback: function(r){
				}
			});
		}, __("Make"));
	}	

});