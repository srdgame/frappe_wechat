# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import requests
import json
from frappe import _
from wechatpy.oauth import WeChatOAuth


def get_context(context):
	if frappe.session.user != 'Guest':
		frappe.local.flags.redirect_location = frappe.form_dict.redirect or "/me"
		raise frappe.Redirect

	app = frappe.form_dict.app
	openid = frappe.form_dict.openid
	redirect = frappe.form_dict.redirect

	if not (app and openid):
		raise frappe.PermissionError("App or Openid does not exists!")

	# context.no_cache = 1
	context.show_sidebar = False

	context.title = _("Binding Wechat")
	context.doc = {
		"app": app,
		"openid": openid,
		"redirect": redirect,
	}
