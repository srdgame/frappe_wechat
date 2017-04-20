# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from wechatpy.oauth import WeChatOAuth
from wechat.api import check_wechat_binding

no_cache = 1
no_sitemap = 1


def get_context(context):
	context.no_cache = 1

	app = check_wechat_binding()
	if app:
		context.redirect_url = "/me"
	else:
		context.redirect_url = "/login"

