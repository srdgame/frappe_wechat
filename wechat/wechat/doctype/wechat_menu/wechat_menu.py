# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import os
import frappe
from frappe.model.document import Document

class WechatMenu(Document):
	pass


@frappe.whitelist()
def query_menu_routes():
	app_path = frappe.get_app_path('wechat')
	folders = frappe.local.flags.web_pages_folders or ('www', 'templates/pages')
	routes = ['']
	prefix = 'wechat_'
	for start in folders:
		search_path = os.path.join(app_path, start)
		for root, dirs, files in os.walk(search_path):
			for file in files:
				if file[-4:] != 'html':
					continue
				if len(file) > len(prefix) and file[0:len(prefix)] == prefix:
					routes.append(file[len(prefix):-5])

	return routes