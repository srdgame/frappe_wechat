# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe import _
from iot.hdb import iot_device_cfg


def get_context(context):
	context.no_cache = 1
	context.show_sidebar = True

	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	try:
		name = frappe.form_dict.device or frappe.form_dict.name
		gateway = frappe.form_dict.gateway or frappe.form_dict.sn
		app = frappe.form_dict.app or frappe.form_dict.app_id
		if not name or not gateway or not app:
			frappe.local.flags.redirect_location = "/"
			raise frappe.Redirect

		context.language = frappe.db.get_value("User", frappe.session.user, ["language"])
		context.csrf_token = frappe.local.session.data.csrf_token

		if 'Company Admin' in frappe.get_roles(frappe.session.user):
			context.isCompanyAdmin = True

		# print(name)
		context.gateway = gateway
		doc = frappe.get_doc('IOT Device', gateway)
		doc.has_permission('read')
		context.doc = doc

		context.device_sn = name

		cfg = iot_device_cfg(gateway, name)
		context.dev_desc = cfg['meta']['inst'] or cfg['meta']['name'] or doc.description or doc.dev_name or "UNKNOWN"
		context.app_id = app

		context.title = _('Wechat Device Data')

	except Exception as ex:
		frappe.logger(__name__).exception(ex)
