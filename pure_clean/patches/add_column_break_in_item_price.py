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
            },	
		]
	}
	
	print('Add Column Break field in Item Price.....')
	create_custom_fields(custom_field, update=True)