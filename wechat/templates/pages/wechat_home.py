# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from wechatpy.oauth import WeChatOAuth
from wechat.api import redirect_to_login

no_cache = 1
no_sitemap = 1


def get_context(context):
	app = frappe.form_dict.app
	if not frappe.session.user or frappe.session.user=='Guest':
		redirect_to_login(app)

	homepage = frappe.get_doc('Wechat Homepage', app)

	context.title = homepage.title or homepage.company

	context.homepage = homepage
