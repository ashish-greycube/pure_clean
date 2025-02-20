frappe.ui.form.on('Sales Order',{

    onload(frm){
        frappe.db.get_single_value('Pure Clean Settings', 'priority_rate')
            .then(priority_rate => {
                if(priority_rate){
                    frm.set_value('extra_rate_percentage_cf', priority_rate)
                }
            })
    },
    before_save(frm){
        if (frm.doc.washing_priority_cf == "Quick"){
            if(frm.doc.extra_rate_percentage_cf){
                for(let item of frm.doc.items){
                    if (item.price_list_rate){
                        let priority_based_rate = item.price_list_rate + ( (item.price_list_rate * frm.doc.extra_rate_percentage_cf)/100 )
                        frappe.model.set_value(item.doctype, item.name, 'rate', priority_based_rate)
                        // item.rate= priority_based_rate
                    }
                }
            }
            else{
                frappe.throw(__("Please set Extra Rate Percentage"))
            }
        }
    }
})