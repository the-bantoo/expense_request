
// Copyright (c) 2020, Bantoo and contributors
// For license information, please see license.txt
frappe.ui.form.on('Expense Entry Item', {
	amount(frm, cdt, cdn) {
        var items = locals[cdt][cdn];
        var total = 0;
        var quantity = 0;
        frm.doc.expenses.forEach(
            function(items) { 
                total += items.amount;
                quantity +=1;
            });
        frm.set_value("total", total);
        refresh_field("total");
        frm.set_value("quantity", quantity);
        refresh_field("quantity");
	}
});
frappe.ui.form.on('Expense Entry', {
    refresh(frm) {
        //update total and qty when an item is added
	},
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
		
	}

});