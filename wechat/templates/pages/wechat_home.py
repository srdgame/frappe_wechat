# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from wechatpy.oauth import WeChatOAuth
from wechat.api import check_wechat_binding


def get_context(context):
	app = check_wechat_binding()
	context.no_cache = 1

	homepage = frappe.get_doc('Wechat Homepage', app)

	context.title = homepage.title or homepage.company

	context.homepage = homepage
