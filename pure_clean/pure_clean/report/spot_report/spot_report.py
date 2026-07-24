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
            "width": "400"
        },
        {
            "fieldname" : "item_code",
            "fieldtype" : "Link",
            "label" : ("Item Code"),
            "options" : "Item",
            "width": "280"
        },
        {
            "fieldname" : "spot_in",
            "fieldtype" : "Int",
            "label" : ("Spot In"),
            "width": "180"
        },
        {
            "fieldname" : "spot_out",
            "fieldtype" : "Int",
            "label" : ("Spot Out"),
            "width": "180"
        },
        {
            "fieldname" : "balance",
            "fieldtype" : "Int",
            "label" : ("Balance"),
            "width": "180"
        },
    ]

def get_data(filters):
    conditions = ""
    values = {}

    # Safely building conditions using dictionary values to prevent SQL injection
    if filters.get("customer"):
        conditions += " AND so.customer = %(customer)s"
        values["customer"] = filters.get("customer")
    
    if filters.get("item"):
        conditions += " AND soi.item_code = %(item)s"
        values["item"] = filters.get("item")
    
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND so.transaction_date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters.get("from_date")
        values["to_date"] = filters.get("to_date")

    return frappe.db.sql(f"""
        SELECT
            so.customer AS customer,
            soi.item_code AS item_code,
            soi.item_name AS item_name,
            SUM(soi.spot_in_cf) AS spot_in,
            SUM(soi.spot_out_cf) AS spot_out,
            (SUM(soi.spot_in_cf) - SUM(soi.spot_out_cf)) AS balance
        FROM
            `tabSales Order` so
        JOIN
            `tabSales Order Item` soi ON soi.parent = so.name
        WHERE 
            so.docstatus != 2
            AND (soi.spot_in_cf != 0 OR soi.spot_out_cf != 0)
            {conditions}
        GROUP BY
            so.customer, soi.item_code
    """, values, as_dict=1)
