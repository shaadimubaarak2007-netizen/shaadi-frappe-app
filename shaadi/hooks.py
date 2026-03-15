app_name = "shaadi"
app_title = "Shaadi"
app_publisher = "Amit Kumar"
app_description = "Indian Matrimonial Platform"
app_email = "hello@amitkumar.live"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "shaadi",
# 		"logo": "/assets/shaadi/logo.png",
# 		"title": "Shaadi",
# 		"route": "/shaadi",
# 		"has_permission": "shaadi.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/shaadi/css/shaadi.css"
# app_include_js = "/assets/shaadi/js/shaadi.js"

# include js, css files in header of web template
# web_include_css = "/assets/shaadi/css/shaadi.css"
# web_include_js = "/assets/shaadi/js/shaadi.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "shaadi/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "shaadi/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "shaadi"

# website user home page (by Role)
role_home_page = {
	"Matrimonial Member": "shaadi",
	"Matrimonial Premium Member": "shaadi",
	"Guest": "shaadi",
	"Website User": "shaadi",
}

# Website Route Rules - Frontend route rules to make frontend the home page
website_route_rules = [
	{"from_route": "/", "to_route": "shaadi"},
	{"from_route": "/home", "to_route": "shaadi"},
	{"from_route": "/account/login", "to_route": "shaadi"},
	{"from_route": "/account/signup", "to_route": "shaadi"},
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "shaadi.utils.jinja_methods",
# 	"filters": "shaadi.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "shaadi.install.before_install"
after_install = "shaadi.shaadi.install.after_install"

# Fixtures
# --------
# Note: Roles and Role Profiles are created programmatically in install.py (ERPNext pattern)
fixtures = [
	{
		"dt": "Subscription Plan"
	},
	{
		"dt": "Workspace",
		"filters": [
			["module", "=", "Shaadi"]
		]
	}
]

# Uninstallation
# ------------

# before_uninstall = "shaadi.uninstall.before_uninstall"
# after_uninstall = "shaadi.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "shaadi.utils.before_app_install"
# after_app_install = "shaadi.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "shaadi.utils.before_app_uninstall"
# after_app_uninstall = "shaadi.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shaadi.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Member Profile": {
		"after_insert": "shaadi.shaadi.utils.notifications.on_profile_created",
		"on_update": "shaadi.shaadi.utils.notifications.on_profile_updated"
	},
	"Match Request": {
		"on_update": "shaadi.shaadi.utils.notifications.on_interest_response"
	},
	"Conversation Message": {
		"after_insert": "shaadi.shaadi.utils.notifications.on_new_message"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"shaadi.shaadi.tasks.daily.expire_subscriptions",
		"shaadi.shaadi.tasks.daily.send_match_digest"
	],
	"cron": {
		"0 8 * * *": [
			"shaadi.shaadi.tasks.daily.precompute_matches"
		]
	}
}

# Testing
# -------

# before_tests = "shaadi.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "shaadi.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "shaadi.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["shaadi.utils.before_request"]
# after_request = ["shaadi.utils.after_request"]

# Job Events
# ----------
# before_job = ["shaadi.utils.before_job"]
# after_job = ["shaadi.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"shaadi.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

