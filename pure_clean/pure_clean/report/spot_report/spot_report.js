// Copyright (c) 2026, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.query_reports["Spot Report"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "from_date",
			"label": __("From"),
			"fieldtype": "Date",
			// "reqd": 1,
			// "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			"fieldname": "to_date",
			"label": __("To"),
			"fieldtype": "Date",
			// "reqd": 1,
			// "default": frappe.datetime.get_today(),
		},
	]
};
