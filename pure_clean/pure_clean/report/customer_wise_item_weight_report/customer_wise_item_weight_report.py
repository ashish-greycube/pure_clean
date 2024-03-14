# Copyright (c) 2024, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, _
from frappe.utils import flt,cstr

def execute(filters=None):
	columns, report_data = [], []

	columns = get_columns(filters)
	report_data = get_data(filters)

	if not report_data:
		msgprint(_("No records found"))
		return columns, report_data
	
	return columns, report_data 

def get_columns(filters):
	return[
		{
			'fieldname':'item_code',
			'label': _('Item Code'),
			'fieldtype':'Link',
			'options': 'Sales Invoice Item',
			'width':'150',
			'align':'right'
		},
		{
			'fieldname':'item_name',
			'label': _('Item Name'),
			'fieldtype':'Link',
			'options': 'Sales Invoice Item',
			'width':'250',
			'align':'right'
		},
		{
			'fieldname':'qty',
			'label': _('Qty'),
			'fieldtype':'Data',
			'width':'120',
			'align':'right'
		},
		{
			'fieldname':'item_price',
			'label': _('Item Price (Per)'),
			'fieldtype':'Data',
			'width':'150',
			'align':'right'
		},
		{
			'fieldname':'total_sales',
			'label': _('Total Sales'),
			'fieldtype':'Currency',
			'width':'150',
			'align':'right'
		},
		{
			'fieldname':'item_weight',
			'label': _('Item Weight (Per)'),
			'fieldtype':'Data',
			'width':'150',
			'align':'right'
		},
		{
			'fieldname':'total_weight',
			'label': _('Total Weight'),
			'fieldtype':'Data',
			'width':'150',
			'align':'right'
		},
	]

def get_data(filters):

	data = frappe.db.sql(""" SELECT i.item_code as item_code,i.item_name as item_name,SUM(i.qty) as qty,i.rate,SUM(i.net_amount) as total_sales,i.item_weight_cf,SUM(i.item_weight_total_cf) as total_weight FROM `tabSales Invoice` as s
INNER JOIN `tabSales Invoice Item` AS i ON i.parent = s.name
WHERE s.posting_date >= %(from_date)s and s.posting_date <= %(to_date)s and s.customer=%(customer)s
group by i.item_code """,
{"from_date":filters.from_date,
 "to_date":filters.to_date,
 "customer":filters.customer}
 ,as_dict=1)

	total_qty = 0
	total_price = 0
	final_total_sales = 0
	total_weight = 0
	final_total_weight = 0

	for row in data:
		item_details = frappe.db.get_list('Item Price',
									filters={
										"item_code":row.item_code,
										"customer":filters.customer,
									},
									fields = ['price_list_rate','item_weight_cf'])

		total_qty = int(total_qty + row.qty)
		final_total_sales = final_total_sales +row.total_sales
		
		if len(item_details)>0:
			row['item_price']=item_details[0].price_list_rate
			row['item_weight']=item_details[0].item_weight_cf
			total_price = total_price + row.rate
			total_weight = total_weight + row.item_weight_cf
			final_total_weight = final_total_weight + row.total_weight

		else :
			row['item_price']= '---'
			row['item_weight']= '---'
			row['total_weight']= '---'
			
	total_weight_in_kg = flt((final_total_weight / 1000),2)
	
	data.append({'item_name':'<b>Total</b>','qty':frappe.bold(total_qty),'item_price':frappe.bold(total_price),'total_sales': cstr(final_total_sales)+'<b>33</b>','item_weight':frappe.bold(total_weight),'total_weight':frappe.bold(str(total_weight_in_kg)) + ' <b>KG</b>'})
	
	return data