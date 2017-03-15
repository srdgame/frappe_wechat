# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import requests
import json
from frappe import _
from iot.iot.doctype.iot_settings.iot_settings import IOTSettings
from wechatpy.oauth import WeChatOAuth


def get_context(context):
	if frappe.session.user != 'Guest':
		frappe.local.flags.redirect_location = frappe.form_dict.redirect or "/me"
		raise frappe.Redirect

	app = frappe.form_dict.app
	openid = frappe.form_dict.openid
	expires_in = frappe.form_dict.expires_in
	redirect = frappe.form_dict.redirect

	if not (app and openid):
		raise frappe.PermissionError("App or Openid does not exists!")

	try:
		user = frappe.get_value("Wechat Binding", {"openid": openid, "app": app}, "user")
		if user:
			frappe.local.flags.redirect_location = frappe.form_dict.redirect or "/me"
			raise frappe.Redirect

		context.no_cache = 1
		context.show_sidebar = False

		context.title = _("Binding Wechat")
		context.doc = {
			"app": app,
			"openid": openid,
			"expires": expires_in
		}
	except Exception, e:
		raise frappe.PermissionError(e)
