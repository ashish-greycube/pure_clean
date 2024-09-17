from __future__ import unicode_literals

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.desk.page.setup_wizard.setup_wizard import make_records


def after_migrate():
    custom_fields = {
        "Company": [
            {
				"fieldname":'section_break_cf',
				"fieldtype":'Section Break',
				"insert_after":'default_discount_account',
				"is_custom_field":1,
				"is_system_generated":0,
            },			
			{
				"fieldname": "expense_account_for_cleaning_ct",
				"label":"Expense Account For Cleaning",
				"fieldtype": "Table",
				"options":'Expense Account For Cleaning',
				"insert_after": 'section_break_cf',
				"is_custom_field":1,
				"is_system_generated":0,
				"no_copy":1,
			},			
        ],
        "Sales Invoice": [
            {
				"fieldname":'washing_priority_cf',
                "label":'Washing Priority',
				"fieldtype":'Select',
				"insert_after":'due_date',
				"is_custom_field":1,
				"is_system_generated":0,
                "options":'Normal\nQuick',
                "default":'Normal',
                "translatable":0
            }
		],
        "Sales Order": [
            {
				"fieldname":'washing_priority_cf',
                "label":'Washing Priority',
				"fieldtype":'Select',
				"insert_after":'order_type',
				"is_custom_field":1,
				"is_system_generated":0,
                "options":'Normal\nQuick',
                "default":'Normal',
                "translatable":0
            }
		]
    }
    print("Add Expense Account For Cleaning custom table in Company and Washing Priority custom field in SI,SO.....")
    for dt, fields in custom_fields.items():
        print("*******\n %s: " % dt, [d.get("fieldname") for d in fields])
    create_custom_fields(custom_fields)