# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from erpnext import get_default_company
from frappe.utils import flt
import erpnext

def execute(filters=None):
	if not filters: filters = {}

	columns, data = [], []

	columns = get_columns()
	report_data,report_summary = get_data(filters)
	
	if not report_data:
		msgprint(_("No records found"))
		return columns,report_data
	
	notes="<b>Notes: </b><br>Total Cost (SAR) Condition : In item price doctype --> customer, price list and  weight(gm) is properly set."
	return columns, report_data, notes, None, report_summary

def get_columns():
	currency_symbol=' ('+erpnext.get_default_currency()+')'
	return [
		{
			"fieldname": "customer",
			"label":_("Customer Name"),
			"fieldtype": "Link",
			"options": "Customer",
			"width":'350'
		},
		{
			"fieldname": "total_sales",
			"label":_("Total Sales "+currency_symbol),
			"fieldtype": "Data",
			"width":'200'
		},
		{
			"fieldname": "total_weight",
			"label":_("Total Weight"+' (gm)'),
			"fieldtype": "Data",
			"width":'200'
		},
		{
			"fieldname": "total_cost",
			"label":_("Total Cost"+currency_symbol),
			"fieldtype": "Data",
			"width":'200'
		},
		{
			"fieldname": "profit",
			"label":_("Profit"+currency_symbol),
			"fieldtype": "Data",
			"width":'200'
		},
	]

def get_total_cost_based_on_expense_account(filters):

	company=get_default_company()
	company_doc = frappe.get_doc("Company",company)
	expense_acct_detail = [d.account for d in company_doc.expense_account_for_cleaning_ct]
	cond = " (%s)" % (", ".join(["%s"] * len(expense_acct_detail)))
	join_list=[company] + expense_acct_detail + [filters.to_date,filters.from_date]
	string_tuple=tuple(join_list)

	data = frappe.db.sql(""" select
			sum(debit) - sum(credit)
		total
from
	`tabGL Entry`
where
	company = %s
	and account in {cond}
	and (posting_date <=  %s
		and posting_date >=  %s)
	and is_opening = 'No'
	and is_cancelled = 0
group by
	account""".format(cond=cond),string_tuple,as_dict=1)

	expense_account_total = 0
	for value in data:
		expense_account_total = expense_account_total + value.total

	return expense_account_total


def get_data(filters):
	currency_symbol=' ('+erpnext.get_default_currency()+')'
	result_to_show=[]

	data_for_all_customer = frappe.db.sql(""" SELECT si.customer ,SUM(i.net_amount) as total_sales,SUM(i.item_weight_total_cf) as total_weight From `tabSales Invoice` AS si 
	INNER JOIN `tabSales Invoice Item` AS i ON si.name=i.parent 
	WHERE si.posting_date >= %(from_date)s AND si.posting_date <= %(to_date)s
	GROUP BY si.customer;  """,
	{
		"from_date":filters.from_date,
		"to_date":filters.to_date,
	},as_dict=1)


	if filters.get('customer'):
		data_for_single_customer = frappe.db.sql(""" SELECT si.customer ,SUM(i.net_amount) as total_sales,SUM(i.item_weight_total_cf) as total_weight From `tabSales Invoice` AS si 
	INNER JOIN `tabSales Invoice Item` AS i ON si.name=i.parent 
	WHERE si.posting_date >= %(from_date)s AND si.posting_date <= %(to_date)s AND si.customer = %(customer)s
	GROUP BY si.customer;  """,
	{
		"from_date":filters.from_date,
		"to_date":filters.to_date,
		"customer":filters.customer
	},as_dict=1)
		result_to_show=data_for_single_customer
	else:
		result_to_show=data_for_all_customer

	total_cost_for_all_customer = get_total_cost_based_on_expense_account(filters)
	total_sales_of_all_customer = 0
	total_weight_of_all_customer = 0
	total_profit_for_all_customer=0
	
	for row in data_for_all_customer:
		total_weight_of_all_customer = total_weight_of_all_customer + row.get('total_weight')
		total_sales_of_all_customer = flt((total_sales_of_all_customer + row.get('total_sales')),2)


	if total_weight_of_all_customer!=0:
		cost_per_weight = flt((total_cost_for_all_customer / (total_weight_of_all_customer/1000)),2)
	else:
		cost_per_weight=0
	for row in data_for_all_customer:
		if row.get('total_weight'):
			total_cost=flt(((cost_per_weight * row.get('total_weight'))/1000),2)
			total_profit_for_all_customer=flt(total_profit_for_all_customer+(row.get('total_sales') -total_cost),2)

	for d in result_to_show:
		if d.get('total_weight'):
			d['total_cost']=flt(((cost_per_weight * d.get('total_weight'))/1000),2)
			d['profit']=flt((d.get('total_sales') - d.get('total_cost')),2)
		else :
			d['total_weight']='---'
			d['total_cost']='---'
			d['profit']='---'
		
	report_summary=[
		{'label':'Total cost as per expense account','value':total_cost_for_all_customer},
		{'label':'Total weight(all customer)','value':str(flt((total_weight_of_all_customer/1000),2))+' Kg'},
		{'label':'Cost per weight(Per Kg)','value':cost_per_weight},
		{'label':'Total sales(all customer)','value':total_sales_of_all_customer},
		{'label':'Total profit(all customer)','value':total_profit_for_all_customer}		
		]


	return result_to_show,report_summary

