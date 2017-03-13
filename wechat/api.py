# -*- coding: utf-8 -*-
# Copyright (c) 2015, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import requests
from frappe import throw, msgprint, _
from frappe.model.document import Document
from frappe.utils import cint
from wechat.doctype.wechat_binding.wechat_binding import wechat_bind, wechat_unbind


def valid_auth_code(app=None, auth_code=None):
	app = app or frappe.get_request_header("AppName")
	if not app:
		throw(_("AppName is required in HTTP Header!"))
	auth_code = auth_code or frappe.get_request_header("AuthorizationCode")
	if not auth_code:
		throw(_("AuthorizationCode is required in HTTP Header!"))
	frappe.logger(__name__).debug(_("App as {0} AuthorizationCode as {1}").format(app, auth_code))

	if auth_code != frappe.get_value("Wechat App", app, "authorization_code"):
		throw(_("Authorization Code is incorrect!"))

	frappe.session.user = frappe.get_value("Wechat App", app, "on_behalf")
	return app


@frappe.whitelist(allow_guest=True)
def check_bind(openid=None):
	app = valid_auth_code()
	if not (openid):
		openid = frappe.form_dict.get('openid')
	return frappe.get_value("Wechat Binding", {"openid":openid, "app": app}, "user")


def get_post_json_data():
	if frappe.request.method != "POST" and frappe.request.method != "PUT":
		throw(_("Request Method Must be POST!"))
	ctype = frappe.get_request_header("Content-Type")
	if "json" not in ctype.lower():
		throw(_("Incorrect HTTP Content-Type found {0}").format(ctype))
	if not frappe.form_dict.data:
		throw(_("JSON Data not found!"))
	return json.loads(frappe.form_dict.data)


@frappe.whitelist(allow_guest=True)
def bind(frm_data=None):
	app = valid_auth_code()
	frm_data = frm_data or get_post_json_data()
	user = frm_data.get("user")
	passwd = frm_data.get("passwd")
	openid = frm_data.get("openid")
	expires = frm_data.get("expires")
	if not (user and passwd and openid):
		throw(_("user, passwd, openid is required!"))

	frappe.logger(__name__).debug(_("Wechat App binding user {0} password {1} openid {2} expires{3}")
									.format(user, passwd, openid, expires))

	frappe.local.login_manager.authenticate(user, passwd)
	if frappe.local.login_manager.user != user:
		throw(_("Username password is not matched!"))

	return wechat_bind(app, user, openid, expires)



@frappe.whitelist(allow_guest=True)
def unbind(user=None):
	app = valid_auth_code()
	user = user or get_post_json_data().get("user")
	if not (user):
		throw(_("user is required!"))

	frappe.logger(__name__).debug(_("Wechat App binding user {0}").format(user))

	return wechat_unbind(app, user)


@frappe.whitelist(allow_guest=True)
def list_iot_devices(user):
	app = valid_auth_code()
	if not (user and sn):
		throw(_("user and sn is required!"))



@frappe.whitelist(allow_guest=True)
def iot_device_data(user, sn):
	app = valid_auth_code()
	if not (user and sn):
		throw(_("user and sn is required!"))

	frappe.session.user = user
	return iot.iot.hdb.iot_device_data(sn)


@frappe.whitelist(allow_guest=True)
def iot_device_cfg(user, sn):
	app = valid_auth_code()
	if not (user and sn):
		throw(_("user and sn is required!"))

	return iot.iot.hdb.iot_device_cfg(sn)



@frappe.whitelist(allow_guest=True)
def get_time():
	valid_auth_code()
	return frappe.utils.now()


@frappe.whitelist(allow_guest=True)
def ping():
	form_data = frappe.form_dict
	if frappe.request and frappe.request.method == "POST":
		if form_data.data:
			form_data = json.loads(form_data.data)
		return form_data.get("text") or "No Text"
	return 'pong'


