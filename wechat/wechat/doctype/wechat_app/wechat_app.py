# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class WechatApp(Document):
	def on_update(self):
		self.update_auth_file()
		# self.update_menu()

	def on_trash(self):
		frappe.delete_doc("Wechat Auth File", self.name)

	def update_menu(self):
		frappe.enqueue('wechat.api.create_wechat_menu', app_name=self.name, enqueue_after_commit=True)

	def update_auth_file(self):
		if frappe.get_value("Wechat Auth File", self.name, "name"):
			frappe.set_value("Wechat Auth File", self.name, "route", self.file_name)
			frappe.set_value("Wechat Auth File", self.name, "content", self.file_content)
		else:
			doc = frappe.get_doc({
				"doctype": "Wechat Auth File",
				"title": self.name,
				"route": self.file_name,
				"app": self.name,
				"content": self.file_content,
			})
			doc.insert(ignore_permissions=True)
