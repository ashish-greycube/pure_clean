# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import calendar

import frappe
from frappe import _
from frappe.utils import cint, cstr, getdate


def execute(filters=None):
	common_columns = [
		{
			"label": _("New Customers"),
			"fieldname": "new_customers",
			"fieldtype": "Int",
			"default": 0,
			"width": 125,
		},
		{
			"label": _("Repeat Customers"),
			"fieldname": "repeat_customers",
			"fieldtype": "Int",
			"default": 0,
			"width": 125,
		},
		{"label": _("Total"), "fieldname": "total", "fieldtype": "Int", "default": 0, "width": 100},
		{
			"label": _("New Customer Revenue"),
			"fieldname": "new_customer_revenue",
			"fieldtype": "Currency",
			"default": 0.0,
			"width": 175,
		},
		{
			"label": _("Repeat Customer Revenue"),
			"fieldname": "repeat_customer_revenue",
			"fieldtype": "Currency",
			"default": 0.0,
			"width": 175,
		},
		{
			"label": _("Total Revenue"),
			"fieldname": "total_revenue",
			"fieldtype": "Currency",
			"default": 0.0,
			"width": 175,
		},
	]

	return get_data_by_time(filters, common_columns)



def get_data_by_time(filters, common_columns):
	# key yyyy-mm
	columns = [
		{"label": _("Year"), "fieldname": "year", "fieldtype": "Data", "width": 100},
		{"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 100},
	]
	columns += common_columns

	customers_in = get_customer_stats(filters)

	# time series
	from_year, from_month, temp = filters.get("from_date").split("-")
	to_year, to_month, temp = filters.get("to_date").split("-")

	from_year, from_month, to_year, to_month = (
		cint(from_year),
		cint(from_month),
		cint(to_year),
		cint(to_month),
	)

	out = []
	for year in range(from_year, to_year + 1):
		for month in range(
			from_month if year == from_year else 1, (to_month + 1) if year == to_year else 13
		):
			key = "{year}-{month:02d}".format(year=year, month=month)
			data = customers_in.get(key)
			new = data["new"] if data else [0, 0.0]
			repeat = data["repeat"] if data else [0, 0.0]
			out.append(
				{
					"year": cstr(year),
					"month": calendar.month_name[month],
					"new_customers": new[0],
					"repeat_customers": repeat[0],
					"total": new[0] + repeat[0],
					"new_customer_revenue": new[1],
					"repeat_customer_revenue": repeat[1],
					"total_revenue": new[1] + repeat[1],
				}
			)
	return columns, out

def get_customer_stats(filters):
	"""Calculates number of new and repeated customers and revenue."""
	company_condition = ""

	if filters.get("sales_person"):
		company_condition = " and sales_person=%(sales_person)s"

	customers = []
	customers_in = {}

	for si in frappe.db.sql(
		"""select
			si.posting_date as posting_date,
			si.customer,
			
			st.sales_person,
			st.allocated_amount
		from
			`tabSales Invoice` si
		Inner join `tabSales Team` st ON st.parent = si.name
		where
			st.idx = 1
			and si.docstatus = 1
			and si.posting_date <= %(to_date)s
			{company_condition}
		order by
			posting_date
		""".format(
			company_condition=company_condition
		),
		filters,
		as_dict=1,
		debug=1
	):

		key = si.posting_date.strftime("%Y-%m")
		new_or_repeat = "new" if si.sales_person not in customers else "repeat"
		customers_in.setdefault(key, {"new": [0, 0.0], "repeat": [0, 0.0]})

		# if filters.from_date <= si.posting_date.strftime('%Y-%m-%d'):
		if getdate(filters.from_date) <= getdate(si.posting_date):
			customers_in[key][new_or_repeat][0] += 1
			customers_in[key][new_or_repeat][1] += si.allocated_amount

		if new_or_repeat == "new":
			customers.append(si.sales_person)
		print(customers_in,"--------------------------------------",customers)

	return customers_in

# def get_customer_stats(filters):
# 	"""Calculates number of new and repeated customers and revenue."""
# 	company_condition = ""

# 	if filters.get("sales_person"):
# 		company_condition = " and sales_person=%(sales_person)s"

# 	customers = []
# 	customers_in = {}
# 	# values = {"sales_person":"Zelam","to_date":"2024-12-31"}
# 	for si in frappe.db.sql(
# 		"""select
# 			si.posting_date as posting_date,
# 			si.customer,
			
# 			st.sales_person,
# 			st.allocated_amount
# 		from
# 			`tabSales Invoice` si
# 		Inner join `tabSales Team` st ON st.parent = si.name
# 		where
# 			st.idx = 1
# 			and si.docstatus = 1
# 			and si.posting_date <= %s
# 			and st.sales_person = %s
# 		order by
# 			posting_date
# 		""",("2024-12-31","Zelam"),
# 		# filters,
# 		as_dict=1,
# 		debug=1
# 	):

# 		key = si.posting_date.strftime("%Y-%m")
# 		new_or_repeat = "new" if si.sales_person not in customers else "repeat"
# 		customers_in.setdefault(key, {"new": [0, 0.0], "repeat": [0, 0.0]})

# 		# if filters.from_date <= si.posting_date.strftime('%Y-%m-%d'):
# 		if getdate(filters.from_date) <= getdate(si.posting_date):
# 			customers_in[key][new_or_repeat][0] += 1
# 			customers_in[key][new_or_repeat][1] += si.allocated_amount

# 		if new_or_repeat == "new":
# 			customers.append(si.sales_person)
# 		print(customers_in,"--------------------------------------",customers)

# 	return customers_in