# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint,_


def execute(filters=None):
	if not filters: filters = {}
	columns, data = [], []

	columns = get_columns()
	data = get_data(filters)
	
	if not data:
		msgprint(_("No records found"))
		return columns,data
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "month",
			"label": _("Month"),
			"fieldtype": "Select",
			"options": "Jan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
			"width":'100'
		},
		{
			"fieldname": "customer",
			"label":_("Customer Name"),
			"fieldtype": "Link",
			"options": "Customer",
			"width":'350'
		},
		{
			"fieldname": "sales_amount",
			"label":_("Sales Amount"),
			"fieldtype": "Currency",
			"width":'200'
		},
		{
			"fieldname": "paid_amount",
			"label":_("Paid Amount"),
			"fieldtype": "Currency",
			"width":'200'
		}
	]

def get_data(filters):
	conditions = get_conditions(filters)
	si_list = frappe.db.sql("""
					SELECT
			name,
			DATE_FORMAT(posting_date, '%b') AS month,
			YEAR(posting_date) AS year,
			customer,
			SUM(base_grand_total) as sales_amount,
			(SUM(base_grand_total)- SUM(outstanding_amount)) as paid_amount
		FROM
			`tabSales Invoice`
		WHERE
			docstatus = 1 
			{0}
		GROUP BY month
		ORDER BY posting_date ASC
			""".format(conditions),as_dict=1,debug=1)
	return si_list

def get_conditions(filters):
	conditions = ""

	if filters.get("fiscal_year"):
		conditions += " and YEAR(posting_date) = '{0}'".format(filters.get("fiscal_year"))

	if filters.get("customer"):
		conditions += " and customer = '{0}'".format(filters.get("customer"))

	if filters.get("month"):
		conditions += " and DATE_FORMAT(posting_date, '%b') = '{0}'".format(filters.get("month"))

	return conditions