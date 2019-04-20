# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from math import ceil
from frappe import _

from wechat.api import check_wechat_binding
from iot_ui.ui_api import devices_list_array


def get_context(context):
	app = check_wechat_binding()

	if frappe.session.user == 'Guest':
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect

	filter = frappe.form_dict.filter
	if not filter:
		filter = "all"
	context.filter = filter
	context.no_cache = 1
	context.show_sidebar = True

	context.language = frappe.db.get_value("User", frappe.session.user, ["language"])
	context.csrf_token = frappe.local.session.data.csrf_token

	if 'Company Admin' in frappe.get_roles(frappe.session.user):
		context.isCompanyAdmin = True
	userdevices = devices_list_array()

	if userdevices:
		context.userdevices = devices_list_array()
		context.dev_lens = int(ceil(len(devices_list_array())*0.1))
	else:
		context.userdevices = []
		context.dev_lens = 0
	context.title = _('Wechat Devices')
