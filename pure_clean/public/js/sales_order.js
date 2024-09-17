frappe.ui.form.on('Sales Order',{
    before_save(frm){
        if (frm.doc.washing_priority_cf == "Quick"){
            frappe.db.get_single_value('Pure Clean Settings', 'priority_rate')
                .then(priority_rate => {
                    if(priority_rate){
                        for(let item of frm.doc.items){
                            if (item.price_list_rate){
                                let priority_based_rate = item.price_list_rate + ( (item.price_list_rate * priority_rate)/100 )
                                frappe.model.set_value(item.doctype, item.name, 'rate', priority_based_rate)
                                // item.rate= priority_based_rate
                            }
                        }
                    }
                    else{
                        frappe.throw(_("Please set Increase rate in Pure Clean Settings"))
                    }
                })
        }
    }
})