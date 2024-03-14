frappe.ui.form.on('Company',{
    setup: function(frm){
        frm.set_query("account","expense_account_for_cleaning_ct", function(){
			return {
				filters: {
                    "account_type": ["in",["Expense Account","Cost of Goods Sold"]],
                    "is_group":0,
                    "disabled":0,
                    "company":frm.doc.name
                },
			}
		});
    }
})