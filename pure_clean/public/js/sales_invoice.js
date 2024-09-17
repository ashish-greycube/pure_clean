frappe.ui.form.on('Sales Invoice',{
    before_save(frm){
        if (frm.doc.washing_priority_cf == "Quick"){
            frappe.db.get_single_value('Pure Clean Settings', 'priority_rate')
                .then(priority_rate => {
                    if(priority_rate){
                        for(let item of frm.doc.items){
                            if (item.price_list_rate){
                                let priority_based_rate = item.price_list_rate + ( (item.price_list_rate * priority_rate)/100 )
                                frappe.model.set_value(item.doctype, item.name, 'rate', priority_based_rate)
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

frappe.ui.form.on('Sales Invoice Item',{
    item_code(frm, cdt, cdn){
        let row = locals[cdt][cdn];
        if(row.item_code && frm.doc.customer && frm.doc.selling_price_list){
            frappe.db.get_list('Item Price', {
                fields: ['item_code', 'price_list', 'customer', 'item_weight_cf'],
                filters: {
                    'item_code': row.item_code,
                    'price_list': frm.doc.selling_price_list,
                    'customer': frm.doc.customer
                }
            }).then(
                records => {
                    if(records.length > 0){
                        let item = records[0];
                        frappe.model.set_value(cdt, cdn, 'item_weight_cf', item.item_weight_cf)
                        frappe.model.set_value(cdt, cdn, 'item_weight_total_cf', item.item_weight_cf)
                    }
                    
                })
            }
    },

    qty(frm, cdt, cdn){
        let row = locals[cdt][cdn];
        if(row.item_weight_cf){
            let total_item_weight = row.qty * row.item_weight_cf
            frappe.model.set_value(cdt, cdn, 'item_weight_total_cf', total_item_weight)
        }
        
    },

    item_weight_total_cf:function(frm, cdt, cdn){
       calculate_item_weight(frm,cdt,cdn)
      },
        items_remove:function(frm, cdt, cdn){
            calculate_item_weight(frm,cdt,cdn)        
    }
})

let calculate_item_weight = function(frm,cdt,cdn){
    let total = 0
    frm.doc.items.forEach(function(item){
        total = total + item.item_weight_total_cf
    })
    frm.set_value("grand_total_item_weight_cf", total);
}