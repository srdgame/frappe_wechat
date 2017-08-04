# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from wechat.api import check_wechat_binding


def get_context(context):
	app = frappe.form_dict.app
	url = frappe.get_value("Wechat App", app, "user_defined_1")
	if not url:
		throw(_("User Defined 1 URL not defined"))
	context.no_cache = 1
	check_wechat_binding(redirect_url=url)