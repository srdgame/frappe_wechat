# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from frappe import _

app_name = "wechat"
app_title = "Wechat"
app_publisher = "Dirk Chang"
app_description = "Wechat Integration"
app_icon = "fa fa-wechat"
app_color = "green"
app_email = "dirk.chang@symid.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/wechat/css/wechat.css"
# app_include_js = "/assets/wechat/js/wechat.js"

# include js, css files in header of web template
# web_include_css = "/assets/wechat/css/wechat.css"
# web_include_js = "/assets/wechat/js/wechat.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "wechat.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "wechat.install.before_install"
# after_install = "wechat.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "wechat.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"wechat.tasks.all"
# 	],
# 	"daily": [
# 		"wechat.tasks.daily"
# 	],
# 	"hourly": [
# 		"wechat.tasks.hourly"
# 	],
# 	"weekly": [
# 		"wechat.tasks.weekly"
# 	]
# 	"monthly": [
# 		"wechat.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "wechat.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "wechat.event.get_events"
# }

website_route_rules = [
	{"from_route": "/wechat", "to_route": "Wechat App"},
	{"from_route": "/wechat/<path:name>", "to_route": "/api/method/wechat.api.wechat",
		"defaults": {
			"doctype": "Wechat App",
			"parents": [{"title": _("Wechat App"), "name": "wechat"}]
		}
	},
	{"from_route": "/wechat/home", "to_route": "Wechat Homepage"},
	{"from_route": "/wechat/home/<path:name>", "to_route": "wechat_homepage",
		"defaults": {
			"doctype": "Wechat Homepage",
			"parents": [{"title": _("Wechat Homepage"), "name": "wechat_home"}]
		}
	}
]