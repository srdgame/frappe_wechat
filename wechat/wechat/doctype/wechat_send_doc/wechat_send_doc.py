# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import time
import frappe
from frappe import throw, _
from frappe.model.document import Document
from wechatpy import WeChatClient
from wechatpy.oauth import WeChatOAuth


class WechatSendDoc(Document):
	def __get_template_id(self):
		template_name_map = {
			'IOT Device Error': 'device_alarm_template',
			'Tickets Ticket': 'tickets_ticket_template',
			'ToDo': 'tickets_ticket_template'
		}
		return template_name_map[self.document_type]

	def on_submit(self):
		frappe.enqueue('wechat.wechat.doctype.wechat_send_doc.wechat_send_doc.wechat_send',
						doc_name=self.name, doc_doc=self)

	def __set_error(self, err):
		self.set("status", 'Error')
		self.set("error_info", err)
		self.save()
		frappe.db.commit()
		throw(err)

	def wechat_send(self):
		if self.docstatus != 1:
			return
		if self.status in ["Error", "Finished"]:
			return

		app_doc = frappe.get_doc("Wechat App", self.app)
		if app_doc.language:
			frappe.local.lang = app_doc.language
		src_doc = frappe.get_doc(self.document_type, self.document_id)
		if not src_doc:
			self.__set_error(("Cannot find doc {0} id {1}").format(self.document_type, self.document_id))

		data = src_doc.run_method("wechat_tmsg_data")
		if not data:
			self.__set_error(("Cannot generate wechat template data for {0}").format(self.document_type))
		url = src_doc.run_method("wechat_tmsg_url")
		if not url:
			self.__set_error(("Cannot generate wechat template url for {0}").format(self.document_type))

		template_id = frappe.get_value('Wechat App', self.app, self.__get_template_id())
		if not template_id:
			self.__set_error(("Cannot find wechat template id for {0} from app {1}").format(self.document_type, self.app))

		client = WeChatClient(app_doc.app_id, app_doc.secret)

		authorize_url = WeChatOAuth(app_doc.app_id, app_doc.secret, "http://" + app_doc.domain + url).authorize_url

		users = self.get("to_users")

		count = 0
		for user in users:
			done = self.__send_wechat_msg(client, user, template_id, authorize_url, data)
			if done:
				count = count + 1

		if count > 0:
			self.set("status", "Partial")
		if count == len(users):
			self.set("status", "Finished")
		self.save()

	def __send_wechat_msg(self, client, user, template_id, url, data):
		if user.status != 'New':
			return True

		frappe.logger(__name__).info("Send template {0} data {1} to user {2} via app {3}"
									 .format(template_id, data, user.user, self.app))
		user_id = frappe.get_value("Wechat Binding", {"app": self.app, "user": user.user}, "openid")
		if not user_id:
			frappe.logger(__name__).warning(_("User {0} has not bind her/his wechat").format(user.user))
			user.set("sent", 1)
			user.set("status", 'Error')
			user.set("info", ("User {0} has not bind her/his wechat").format(user.user))
			return True

		try:
			r = client.message.send_template(user_id, template_id, url, top_color='yellow', data=data)

			if r["errcode"] == 0:
				frappe.logger(__name__).debug(_("Send template message ok {0}").format(r))
				user.set("status", 'Finished')
			else:
				frappe.logger(__name__).error(_("Send template message to user {0} failed {1}").format(user.user, r))
				user.set("status", 'Error')

			user.set("sent", 1)
			user.set("info", "result: {0}".format(r))
			return True
		except Exception, e:
			frappe.logger(__name__).error(_("Send template message to user {0} failed {1}").format(user.user, e.message))
			user.set("sent", 1)
			user.set("status", 'Error')
			user.set("info", e.message)
		return False


def wechat_send(doc_name, doc_doc=None):
	doc = doc_doc or frappe.get_doc('Wechat Send Doc', doc_name)
	return doc.wechat_send()


def wechat_notify():
	for doc in frappe.get_all("Wechat Send Doc", "name", filters={"status": ["in", ["New", "Partial"]], "docstatus": 1}):
		frappe.enqueue('wechat.wechat.doctype.wechat_send_doc.wechat_send_doc.wechat_send',
						doc_name=doc.name)


@frappe.whitelist()
def wechat_resend(doc_name):
	doc = frappe.get_doc("Wechat Send Doc", doc_name)
	doc.amend()
