# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document


class WechatBinding(Document):
	pass


def on_doctype_update():
	"""Add indexes in `Wechat Binding`"""
	frappe.db.add_index("Wechat Binding", ["app", "user"])


def wechat_bind(app, user, openid, expires=None):
	doc_name = frappe.get_value("Wechat Binding", {"user" : user, "app" : app})
	if doc_name:
		frappe.set_value("Wechat Binding", doc_name, "openid", openid)
		frappe.set_value("Wechat Binding", doc_name, "expires", expires)
		return _("Binding is done")

	doc = frappe.get_doc({
		"doctype": "Wechat Binding",
		"user": user,
		"app": app,
		"openid": openid,
		"expires": expires
	})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()

	return _("Binding is done")


def wechat_unbind(app, user):
	name = frappe.get_value("Wechat Binding", {"app": app, "user": user})
	if not name:
		throw(_("There is no binding for App{0} User{1}").format(app, user))

	frappe.delete_doc("Wechat Binding", name, ignore_permissions=True)
	frappe.db.commit()

	return _("Binding has ben deleted")