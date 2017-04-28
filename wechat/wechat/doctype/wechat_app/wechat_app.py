# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class WechatApp(Document):
	def on_update(self):
		self.create_auth_file()
		self.update_menu()

	def update_menu(self):
		frappe.enqueue('wechat.api.create_wechat_menu', app_name=self.name)

	def create_auth_file(self):
		frappe.delete_doc("Wechat Auth File", self.name, ignore_permissions=True)
		doc = frappe.get_doc({
			"doctype": "Wechat Auth File",
			"title": self.name,
			"route": self.file_name,
			"app": self.name,
			"content": self.file_content,
		})
		doc.insert(ignore_permissions=True)
