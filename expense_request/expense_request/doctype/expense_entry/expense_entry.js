// Copyright (c) 2020, Bantoo and contributors
// For license information, please see license.txt

function update_totals(frm, cdt, cdn){
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

frappe.ui.form.on('Expense Entry Item', {
	amount(frm, cdt, cdn) {
        update_totals(frm, cdt, cdn);
	},
	expenses_remove(frm, cdt, cdn){
        update_totals(frm, cdt, cdn);
	}
	
});


frappe.ui.form.on('Expense Entry', {
    before_save: function(frm) { 
        
        //issue: if both dcc and cc are not set before save, changing dcc doesnt register in the code
        //frm.refresh_field('default_cost_center');
        
        frm.refresh();

        $.each(frm.doc.expenses, function(i, d) { 
            let count = 0;
            
            if((d.cost_center === "" || typeof d.cost_center == 'undefined')) { 
                
                if (count > 0) {
                    return false;
                }
                
                if (frm.default_cost_center === "" || typeof frm.default_cost_center == 'undefined') {
                    frappe.validated = false;
                    frappe.msgprint("Set a Default Cost Center or ensure all expenses with account <strong>" 
                                    + d.expense_account + "</strong> have a Cost Center.");
                    //return false;
                }
                else {
                    d.cost_center = frm.default_cost_center; 
                }
                count += 1;
                
            } 
            
        }); 
        
    },
    refresh(frm) {
        //update total and qty when an item is added
	},
	onload(frm) {
	    //console.log("hello");

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