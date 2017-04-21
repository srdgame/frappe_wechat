# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

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
