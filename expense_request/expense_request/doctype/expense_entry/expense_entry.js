// Copyright (c) 2020, Bantoo and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Entry', {
	onload(frm) {
		frm.set_query("expense_account", 'expenses', () => {
			return {
				filters: [
					["Account", "parent_account", "Like", "%Expenses%"]
				]
			}
		});
		frm.set_query("cost_center", 'expenses', () => {
			return {
				filters: [
					["Cost Center", "is_group", "=", "0"]
				]
			}
		});
		frm.set_query("default_cost_center", () => {
			return {
				filters: [
					["Cost Center", "is_group", "=", "0"]
				]
			}
		});
		
	},
	refresh: function(frm) {
		frm.add_custom_button(__('Journal Entry'), function(){
			frappe.call({
				method: "expense_request.api.initialise_journal_entry",
				args: {
					expense_entry_name: frm.doc.name
				},
				callback: function(r){
				}
			});
		}, __("Make"));
	}	

});