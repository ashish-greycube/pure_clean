import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_field = {
		"Sales Invoice Item": [
			{
				"fieldname":'item_weight_cf',
				"label":"Weight (Per)",
				"fieldtype":'Float',
				"insert_after": 'item_tax_template',
				"is_custom_field":1,
				"in_list_view":1,
				"is_system_generated":0,
				"translatable":0,
				"no_copy":1,
				"precision": 1,
				"read_only":1
				
            },			
			{
				"fieldname": "item_weight_total_cf",
				"label":"Total Weight",
				"fieldtype": "Float",
				"insert_after": 'item_weight_cf',
				"is_custom_field":1,
				"in_list_view":1,
				"is_system_generated":0,
				"translatable":0,
				"no_copy":1,
				"precision": 1,
				"read_only":1
			},			
		]
	}
	
	print('Add Weight and Total Item Weight field in Sales Invoice Item.....')
	create_custom_fields(custom_field, update=True)