# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class WechatApp(Document):
	def on_update(self):
		frappe.enqueue('wechat.api.create_wechat_menu', app_name=self.name)

