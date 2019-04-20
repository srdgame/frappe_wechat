# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from wechat.api import check_wechat_binding


def get_context(context):
	app = check_wechat_binding()

	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	context.no_cache = 1
	context.show_sidebar = True

	context.language = frappe.db.get_value("User", frappe.session.user, ["language"])
	context.csrf_token = frappe.local.session.data.csrf_token

	if 'Company Admin' in frappe.get_roles(frappe.session.user):
		context.isCompanyAdmin = True

	context.wechat_openid = frappe.db.get_value("Wechat Binding", {"user": frappe.session.user, "app": app}, "openid")

	context.user_id = frappe.session.user
	context.wechat_app = app
	context.title = _('Wechat Unbind')
