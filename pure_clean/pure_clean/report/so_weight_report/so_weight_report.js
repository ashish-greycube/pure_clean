// Copyright (c) 2025, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */
var d  = new Date()
frappe.query_reports["SO Weight Report"] = {
	"filters": [
		{
			fieldname : 'from_date',
			fieldtype : 'Date',
			label : __('From Date'),
			default : new Date(d.getFullYear(), d.getMonth(), 1),
			reqd : 1
		},
		{
			fieldname : 'to_date',
			fieldtype : 'Date',
			label : __('To Date'),
			default : 'Today',
			reqd : 1
		},
		{
			fieldname : 'customer',
			fieldtype : 'Link',
			label : __('Customer'),
			options : 'Customer',
		},
		{
			fieldname : 'machine',
			fieldtype : 'Link',
			label : __('Machine'),
			options : 'Machines',
		},
		{
			fieldname : 'chemical',
			fieldtype : 'Link',
			label : __('Chemical'),
			options : 'Chemicals',
		}
	]
};
