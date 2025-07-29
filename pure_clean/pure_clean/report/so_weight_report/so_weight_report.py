# Copyright (c) 2025, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
import erpnext
from frappe import _
from frappe.utils import today, flt, add_to_date
def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data, summary = get_data(filters)

	if not data:
		frappe.msgprint(_("No records found"))
		return columns,data
	
	return columns, data, None, None, summary

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
			'fieldtype' : 'Data',
			'label' : _('Machine'),
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
			'fieldtype' : 'Data',
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
	data = []
	summary = []
	reportData = []
	query_data = frappe.db.sql('''
					SELECT 
						tso.transaction_date AS "date", 
						tso.customer AS "customer", 
						tso.name AS "so_no", 
						tso.grand_total AS "sales_amount",
						m.machine_name AS "machine",
						IF(tso.grand_total_item_weight_cf > 0, tso.grand_total_item_weight_cf / 1000, tso.grand_total_item_weight_cf) AS "weight",
						m.time AS "machine_time",
						tso.chemical_cf as "chemical_type"
					FROM `tabSales Order` tso
					INNER JOIN `tabMachine Details` m
					ON m.parent = tso.name
					WHERE tso.transaction_date BETWEEN '{0}' AND '{1}' AND tso.docstatus = 1
					{2}
					ORDER BY tso.name;
				'''.format(filters.get('from_date'), filters.get('to_date'), conditions) ,as_dict = 1)
	
	if len(query_data) > 0:
		parent = query_data[0]['so_no']
		one_so_machines_time = []
		one_so_machines = []
		row = {
			'date' : query_data[0]['date'],
			'customer' : query_data[0]['customer'],
			'so_no' : query_data[0]['so_no'],
			'sales_amount' : query_data[0]['sales_amount'],
			'weight' : query_data[0]['weight'],
			'chemical_type' : query_data[0]['chemical_type']
		}
		for qd in query_data:
			# print(qd)
			if qd['so_no'] == parent:
				if qd['machine'] != None:
					one_so_machines.append(qd['machine'])
				if qd['machine_time'] != None:
					one_so_machines_time.append(str(qd['machine_time']))
			elif qd['so_no'] != parent:
				# print(one_so_machines, "=============")
				if len(one_so_machines) > 0 and len(one_so_machines_time) > 0:
					row.update({
						'machine' : ', '.join(one_so_machines),
						'machine_time' : ', '.join(one_so_machines_time)
					})
				data.append(row)
				
				parent = qd['so_no']
				row = {
					'date' : qd['date'],
					'customer' : qd['customer'],
					'so_no' : qd['so_no'],
					'sales_amount' : qd['sales_amount'],
					'weight' : qd['weight'],
					'chemical_type' : qd['chemical_type'],
				}
				one_so_machines = [qd['machine']]
				one_so_machines_time = [str(qd['machine_time'])]
		# print(one_so_machines, "----------------")
		if len(one_so_machines) > 0 and len(one_so_machines_time) > 0:
			row.update({
				'machine' : ', '.join(one_so_machines),
				'machine_time' : ', '.join(one_so_machines_time)
			})
		data.append(row)

		reportData, cost_per_kg, material_accounts_total, total_so_weight = calculate_cost_for_each_so(data,filters)
		
		summary = [
			{'label' : _('Total Amount Of Material Account(From Company)'), 'value' : flt(material_accounts_total, 2),  "datatype": "Currency",  "indicator": "Green" },
			{'label' : _('Total Weight(All SO)'), 'value' : str(flt(total_so_weight, 2))+' KG',  "indicator": "Blue" },
			{'label' : _('Cost Per KG'), 'value' : flt(cost_per_kg, 2),  "indicator": "Red" }
		]
		
		if filters.get('machine'):
			reportData = get_machine_wise_filter_data(filters.get('machine'), reportData, cost_per_kg)
	return reportData, summary

def calculate_cost_for_each_so(data,so_filters):
	accounts = []
	company = erpnext.get_default_company()
	company_doc = frappe.get_doc("Company", company)

	for acc in company_doc.default_material_accounts_cf:
		accounts.append(acc.material_account)
	
	from erpnext.accounts.report.general_ledger.general_ledger import execute as _execute
	filters = frappe._dict({
		'company' : company,
		'from_date' : so_filters.get("from_date"),
		'to_date' : so_filters.get("to_date"),
		'account' : accounts,
		'group_by' : 'Group by Voucher (Consolidated)'
	})
	general_ledger_data = _execute(filters)
	general_ledger_data = general_ledger_data[1]
	material_accounts_total = 0
	if general_ledger_data != [] or None:
		for d in general_ledger_data:
			if d.get('account') == "'Total'":
				material_accounts_total = d.get('balance')

	total_so_weight = 0
	for d in data:
		total_so_weight = total_so_weight + d['weight']
	
	cost_per_kg = 0
	if total_so_weight != 0 or None:
		cost_per_kg = flt(material_accounts_total,2) / total_so_weight
	
	for d in data:
		d.update({
			'cost' : d['weight'] * flt(cost_per_kg, 2)
		})
	return data, cost_per_kg, material_accounts_total, total_so_weight

def get_machine_wise_filter_data(machine, data, cost_per_kg):
	filteredData = []
	for d in data:
		if machine == d['machine'] or machine in d['machine']:
			filteredData.append(d)
	
	if filteredData != [] or None:
		for data in filteredData:
			capacity_map = { 'total' : 0 }
			so_doc = frappe.get_doc("Sales Order", data['so_no'])
			for m in so_doc.machine_table_cf:
				capacity_map[m.machine_name] = [m.capacity, m.time]
				capacity_map['total'] = capacity_map['total'] + m.capacity
			
			data.update({
				'machine' : machine,
				'machine_time' : capacity_map[machine][1]
			})

			if capacity_map['total'] > 0:
				conversion_factor = data['weight'] / capacity_map['total']
				total_weight = conversion_factor * capacity_map[machine][0]
				total_cost = total_weight * flt(cost_per_kg, 2)
				data.update({
					'weight' : total_weight,
					'cost' : total_cost,
				})
	return filteredData