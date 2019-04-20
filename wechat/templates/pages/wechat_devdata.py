# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe import _
from wechat.api import check_wechat_binding
from iot.hdb import iot_device_tree


def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	name = frappe.form_dict.device or frappe.form_dict.name
	if not name:
		frappe.local.flags.redirect_location = "/"
		raise frappe.Redirect

	context.no_cache = 1
	context.show_sidebar = True

	context.language = frappe.db.get_value("User", frappe.session.user, ["language"])
	context.csrf_token = frappe.local.session.data.csrf_token

	if 'Company Admin' in frappe.get_roles(frappe.session.user):
		context.isCompanyAdmin = True

	# print(name)
	context.devsn = name
	doc = frappe.get_doc('IOT Device', name)
	doc.has_permission('read')
	context.doc = doc

	context.dev_desc = doc.description or doc.dev_name or "UNKNOWN"
	context.devices = iot_device_tree(name)

	context.title = _('Wechat Device Data')
