// Copyright (c) 2024, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Customer Loyalty By Sales Partner"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_end_date"),
			"reqd": 1
		},
		{
			"fieldname":"sales_partner",
			"label": __("Sales Partner"),
			"fieldtype": "Link",
			"options":"Sales Partner",
			// "reqd": 1
		}
	],
	'formatter': function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.total) {
			value = "<span style='color:#2728C1'>" + value.bold() + "</span>"
		}
		return value;
	}
};
