import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_field = {
		"Item Price": [
			{
				"fieldname": "item_weight_cf",
				"label":"Weight",
				"fieldtype": "Float",
				"insert_after": 'column_break_2',
				"is_custom_field":1,
				"is_system_generated":0,
				"allow_on_submit":1,
				"translatable":0,
				"no_copy":1,
				"precision": 1,
				"description":'gm'
			},			
		]
	}
	
	print('Add Item Weight CF field in Item Price.....')
	create_custom_fields(custom_field, update=True)