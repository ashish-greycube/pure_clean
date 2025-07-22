# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			'fieldname' : 'date',
			'fieldtype' : 'Date',
			'label' : _('Date'),
			'width' : 130
		},
		{
			'fieldname' : 'customer',
			'fieldtype' : 'Link',
			'label' : _('Customer'),
			'options' : 'Customer',
			'width' : 130
		},
		{
			'fieldname' : 'so_no',
			'fieldtype' : 'Link',
			'label' : _('SO No'),
			'options' : 'Sales Order',
			'width' : 130
		},
		{
			'fieldname' : 'sales_amount',
			'fieldtype' : 'Currency',
			'label' : _('Sales Amount'),
			'width' : 130
		},
		{
			'fieldname' : 'machine',
			'fieldtype' : 'Link',
			'label' : _('Machine'),
			'options' : 'Machines',
			'width' : 130
		},
		{
			'fieldname' : 'weight',
			'fieldtype' : 'Float',
			'label' : _('Weight'),
			'width' : 130
		},
		{
			'fieldname' : 'machine_time',
			'fieldtype' : 'Time',
			'label' : _('Machine Time'),
			'width' : 130
		},
		{
			'fieldname' : 'chemical_type',
			'fieldtype' : 'Link',
			'label' : _('Chemical Type'),
			'options' : 'Chemicals',
			'width' : 130
		},
		{
			'fieldname' : 'cost',
			'fieldtype' : 'Currency',
			'label' : _('Cost'),
			'width' : 130
		},
	]
	return columns

def get_conditions(filters):
	conditions = " "
	if filters.get('customer'):
		conditions += " AND tso.customer = '{0}'".format(filters.get('customer'))

	if filters.get('chemical'):
		conditions += " AND tso.chemical_cf = '{0}'".format(filters.get('chemical'))
	return conditions

def get_data(filters):
	conditions = get_conditions(filters)
	data = frappe.db.sql('''
		SELECT 
			tso.transaction_date AS "date", 
			tso.customer AS "customer", 
			tso.name AS "so_no", 
			tso.grand_total AS "sales_amount",
			m.machine_name AS "machine",
			tso.total_net_weight AS "weight",
			m.time AS "machine_time",
			tso.chemical_cf as "chemical_type"
		FROM `tabSales Order` tso
		INNER JOIN `tabMachine Details` m
		ON m.parent = tso.name
		WHERE tso.transaction_date BETWEEN '{0}' AND '{1}' 
		{2};
	'''.format(filters.get('from_date'), filters.get('to_date'), conditions)
	,as_dict = 1, debug = 1)

	return data