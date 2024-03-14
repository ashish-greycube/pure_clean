import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_field = {
		"Item Price": [
			{
				"fieldname":'column_break_2',
				"fieldtype":'Column Break',
				"insert_after": 'price_list_rate',
				"is_custom_field":1,
				"is_system_generated":0,
            },			
			{
				"fieldname": "item_weight_cf",
				"label":"Weight (gm)",
				"fieldtype": "Float",
				"insert_after": 'column_break_2',
				"is_custom_field":1,
				"is_system_generated":0,
				"translatable":0,
				"no_copy":1,
				"precision": 1,
			},			
		]
	}
	
	print('Add Item Weight CF field in Item Price.....')
	create_custom_fields(custom_field, update=True)