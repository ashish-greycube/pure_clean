from __future__ import unicode_literals
import frappe, erpnext
import frappe.defaults
from frappe import msgprint, _
from frappe.utils import flt

def calculate_item_weight(self,method):
    
    total_item_weight = 0
    for row in self.get('items'):
        item_details = frappe.db.get_all('Item Price',
                              filters={
                                  'customer':self.customer,
                                  'price_list':self.selling_price_list,
                                  'item_code':row.item_code
                              },
                              fields=['item_weight_cf'])
        if len(item_details) > 0:
            row.item_weight_cf = item_details[0].item_weight_cf
            row.item_weight_total_cf = row.qty * row.item_weight_cf
            
            total_item_weight = total_item_weight + row.item_weight_total_cf
    
    self.grand_total_item_weight_cf = total_item_weight

        
    