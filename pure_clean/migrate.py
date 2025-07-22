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
            {
				"fieldname":'material_section_break_cf',
				"fieldtype":'Section Break',
				"insert_after":'expense_account_for_cleaning_ct',
				"is_custom_field":1,
				"is_system_generated":0,
            },			
			{
				"fieldname": "default_material_accounts_cf",
				"label":"Default Material Accounts",
				"fieldtype": "Table",
				"options":'Material Accounts',
				"insert_after": 'material_section_break_cf',
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
            },
            {
				"fieldname":'extra_rate_percentage_cf',
                "label":'Extra Rate Percentage %',
				"fieldtype":'Percent',
				"insert_after":'tax_id',
				"is_custom_field":1,
				"is_system_generated":0,
                "translatable":0,
                "depends_on":"eval: doc.washing_priority_cf == 'Quick'"
            },
			{
                "fieldname" : "machines_section_cf",
                "fieldtype" : "Section Break",
                "insert_after":'set_warehouse',
				"is_custom_field":1,
				"is_system_generated":0,
			},
            {
                "fieldname" : "chemical_cf",
                "fieldtype" : "Link",
                "label":'Chemical',
                "insert_after":'machines_section_cf',
				"is_custom_field":1,
				"is_system_generated":0,
                "options" : "Chemicals",
			},
            {
                "fieldname" : "time_cf",
                "fieldtype" : "Time",
                "label":'Time',
                "insert_after":'chemical_cf',
				"is_custom_field":1,
				"is_system_generated":0,
			},
            {
                "fieldname" : "machine_table_cf",
                "fieldtype" : "Table",
                "label":'Machine Details',
                "insert_after":'time_cf',
				"is_custom_field":1,
				"is_system_generated":0,
                "options" : "Machine Details"
			},
            {
                "fieldname" : "grand_total_item_weight_cf",
                "fieldtype" : "Float",
                "label":'Total Item Weight(GM)',
                "insert_after":'base_net_total',
				"is_custom_field":1,
				"is_system_generated":0,
                "read_only" : 1
            } 
		],

        "Sales Order Item" : [
            {
                "fieldname" : "item_weight_cf",
                "fieldtype" : "Float",
                "label":'Weight (Per)',
                "insert_after":'amount',
				"is_custom_field":1,
				"is_system_generated":0,
			},
            {
                "fieldname" : "item_weight_total_cf",
                "fieldtype" : "Float",
                "label":'Total Weight',
                "insert_after":'stock_uom_rate',
				"is_custom_field":1,
				"is_system_generated":0,
			},
        ]
    }
    print("Add Expense Account For Cleaning custom table in Company and Washing Priority custom field in SI,SO.....")
    for dt, fields in custom_fields.items():
        print("*******\n %s: " % dt, [d.get("fieldname") for d in fields])
    create_custom_fields(custom_fields)