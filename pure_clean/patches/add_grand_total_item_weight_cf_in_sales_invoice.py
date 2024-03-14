import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_field = {
		"Sales Invoice": [	
			{
				"fieldname":'grand_total_item_weight_cf',
				"label":"Total Item Weight (gm)",
				"fieldtype":'Float',
				"insert_after": 'base_net_total',
				"is_custom_field":1,
				"is_system_generated":0,
				"translatable":0,
				"no_copy":1,
				"precision": 1,
				"read_only":1
				
            }			
		]
	}
	
	print('Add Total Item Weight custom field in Sales Invoice.....')
	create_custom_fields(custom_field, update=True)