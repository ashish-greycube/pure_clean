from . import __version__ as app_version

app_name = "pure_clean"
app_title = "Pure Clean"
app_publisher = "GreyCube Technologies"
app_description = "Customization for Pure Clean"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/pure_clean/css/pure_clean.css"
# app_include_js = "/assets/pure_clean/js/pure_clean.js"

# include js, css files in header of web template
# web_include_css = "/assets/pure_clean/css/pure_clean.css"
# web_include_js = "/assets/pure_clean/js/pure_clean.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pure_clean/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Invoice" : "public/js/sales_invoice.js",
              "Company" : "public/js/company.js",
              "Sales Order" : "public/js/sales_order.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "pure_clean.install.before_install"
# after_install = "pure_clean.install.after_install"
after_migrate = "pure_clean.migrate.after_migrate"

# Uninstallation
# ------------

# before_uninstall = "pure_clean.uninstall.before_uninstall"
# after_uninstall = "pure_clean.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pure_clean.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
        "validate":"pure_clean.api.calculate_item_weight"
	}, 
    "Sales Order" : {
        "validate" : ["pure_clean.api.calculate_so_items_weight"],
        "on_submit" : "pure_clean.api.validate_item_weight_with_machine_capacity",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"pure_clean.tasks.all"
#	],
#	"daily": [
#		"pure_clean.tasks.daily"
#	],
#	"hourly": [
#		"pure_clean.tasks.hourly"
#	],
#	"weekly": [
#		"pure_clean.tasks.weekly"
#	]
#	"monthly": [
#		"pure_clean.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "pure_clean.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "pure_clean.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "pure_clean.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["pure_clean.utils.before_request"]
# after_request = ["pure_clean.utils.after_request"]

# Job Events
# ----------
# before_job = ["pure_clean.utils.before_job"]
# after_job = ["pure_clean.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"pure_clean.auth.validate"
# ]

