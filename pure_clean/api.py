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

        
def calculate_so_items_weight(self, method=None):
    total_item_weight = 0
    if len(self.items) > 0:
        for item in self.items:
            per_item_weight = item.item_weight_cf
            item_qty = item.qty
            item.item_weight_total_cf = per_item_weight * item_qty
            print(item_qty, per_item_weight)

            total_item_weight = total_item_weight + (per_item_weight * item_qty)

        self.grand_total_item_weight_cf = total_item_weight

def validate_item_weight_with_machine_capacity(self, method=None):
    machine_capacity = 0
    if self.grand_total_item_weight_cf:
        if len(self.machine_table_cf)>0:
            for machine in self.machine_table_cf:
                if machine.capacity:
                    machine_capacity = machine_capacity + machine.capacity

        total_item_weight_in_kg = self.grand_total_item_weight_cf / 1000  # Convert gm to kg
        if total_item_weight_in_kg > machine_capacity: 
            frappe.throw(_("Total Item Weight {0} KG is greater than Machine Capacity {1} KG").format(
                total_item_weight_in_kg, machine_capacity))