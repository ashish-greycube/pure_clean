# Copyright (c) 2026, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters : filters = {}
    columns, data = [], []
 
    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "fieldname" : "customer",
            "fieldtype" : "Link",
            "label" : ("Customer"),
            "options" : "Customer",
            "width": "300"
        },
        {
            "fieldname" : "item_name",
            "fieldtype" : "Link",
            "label" : ("Item Name"),
            "options" : "Item",
            "width": "180"
        },
        {
            "fieldname" : "spot_in",
            "fieldtype" : "Int",
            "label" : ("Spot In"),
        },
        {
            "fieldname" : "spot_out",
            "fieldtype" : "Int",
            "label" : ("Spot Out"),
        },
        {
            "fieldname" : "balance",
            "fieldtype" : "Int",
            "label" : ("Balance"),
        },
    ]

def get_data(filters):

    conditions = {}

    if filters.get("customer"):
        conditions["customer"] = "AND so.customer = '{0}'".format(filters["customer"])
    
    if filters.get("item"):
        conditions["item"] = "AND soi.item_code = '{0}'".format(filters["item"])
    
    if filters.get("from_date") and filters.get("to_date"):
        conditions["date"] = "AND so.transaction_date BETWEEN '{0}' AND '{1}'".format(filters["from_date"], filters["to_date"])

    return frappe.db.sql("""
		SELECT
			so.customer AS customer,
			soi.item_code AS item_name,
			soi.spot_in_cf AS spot_in,
			soi.spot_out_cf AS spot_out,
			(soi.spot_in_cf - soi.spot_out_cf) AS balance
		FROM
			`tabSales Order` so
		JOIN
			`tabSales Order Item` soi
		ON soi.parent = so.name
		WHERE so.docstatus != 2
            {0} {1} {2}
    """.format(conditions.get("customer") or "", conditions.get("item") or "", conditions.get("date") or ""), as_dict=1, debug=1)
