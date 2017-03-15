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
from frappe.utils.response import build_response
from wechat.doctype.wechat_binding.wechat_binding import wechat_bind, wechat_unbind
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from wechatpy import WeChatClient
from wechatpy.oauth import WeChatOAuth

def redirect_to_login(app):
	code = frappe.form_dict.code
	url = "/wechat_login?app=" + app + "&code=" + code
	redirect = frappe.form_dict.redirect
	if redirect:
		url = url + "&redirect=" + redirect
	frappe.local.flags.redirect_location = url
	raise frappe.Redirect


def get_post_json_data():
	if frappe.request.method != "POST" and frappe.request.method != "PUT":
		throw(_("Request Method Must be POST!"))
	ctype = frappe.get_request_header("Content-Type")
	if "json" not in ctype.lower():
		throw(_("Incorrect HTTP Content-Type found {0}").format(ctype))
	if not frappe.form_dict.data:
		throw(_("JSON Data not found!"))
	return json.loads(frappe.form_dict.data)


@frappe.whitelist()
def iot_device_list(user):
	if not user:
		throw(_("user is required!"))

	frappe.session.user = user

	from iot import hdb_api
	return hdb_api.list_iot_devices(user)


@frappe.whitelist()
def iot_device_data(user, sn):
	if not user and sn:
		throw(_("user and sn is required!"))

	frappe.session.user = user

	from iot import hdb
	return hdb.iot_device_data(sn)


@frappe.whitelist()
def iot_device_cfg(user, sn):
	if not (user and sn):
		throw(_("user and sn is required!"))

	from iot import hdb
	return hdb.iot_device_cfg(sn)


@frappe.whitelist()
def send_wechat_msg(app, users, msg):
	if not frappe.get_value('Wechat App', app):
		throw(_("wechat not existed!"))

	ids = [d[0] for d in frappe.db.get_values('Wechat Binding', {"app": app, "user": ["in", users]}, "openid")]
	print("Wechat sending notify : {0} to openids {1} via app {2}".format(msg, ids, app))


@frappe.whitelist(allow_guest=True)
def get_time():
	return frappe.utils.now()


def fire_raw_content(content, status=200, content_type='text/html'):
	"""
	I am hack!!!
	:param content: 
	:param content_type: 
	:return: 
	"""
	frappe.response['http_status_code'] = status
	frappe.response['filename'] = ''
	frappe.response['filecontent'] = content
	frappe.response['content_type'] = content_type
	frappe.response['type'] = 'download'


@frappe.whitelist(allow_guest=True)
def bind(app, openid, user, passwd, expires=None, redirect=None):
	redirect = redirect or "/desk#desktop"
	if not (app and openid and user and passwd):
		return fire_raw_content("App, OpenID, User, Passwd is required!", 403)

	frappe.local.login_manager.authenticate(user, passwd)
	if frappe.local.login_manager.user != user:
		throw(_("Username password is not matched!"))

	frappe.local.login_manager.user = user
	frappe.local.login_manager.post_login()

	frappe.session.user = 'Administrator'
	wechat_bind(app, user, openid, expires)
	frappe.session.user = user

	if redirect:
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = redirect if frappe.local.response.get('message') == 'Logged In' else "/"

	return _("Wechat binded!")


def create_wechat_menu(app_name):
	print('--------------------------------------------------------')
	app_id = frappe.get_value('Wechat App', app_name, 'app_id')
	secret = frappe.get_value('Wechat App', app_name, 'secret')

	# Top Menu
	top_menu_list = frappe.get_all("Wechat AppMenu",
									filters={'parent': app_name, 'group_index': 0},
									fields=["menu", "alias", "`group`"],
									order_by="`group`")
	menu_buttons = []
	for menu in top_menu_list:
		doc = frappe.get_doc("Wechat Menu", menu.menu)
		menu_button = {
			"type": doc.menu_type or "view",
			"name": menu.alias or doc.menu_name
		}
		if doc.route:
			url = "http://mm.symgrid.com/wechat/" + doc.route + "/" + app_name
		else:
			url = "http://mm.symgrid.com/wechat/home/" + app_name
		menu_button["url"] = WeChatOAuth(app_id, secret, url).authorize_url

		# Sub menu
		sub_menu_list = frappe.get_all("Wechat AppMenu",
										filters={'parent': app_name, '`group`': menu.group},
										fields=["menu", "alias", "group_index"],
										order_by="group_index")

		for sub_menu in sub_menu_list:
			if sub_menu.group_index == 0:
				continue
			if not menu_button.has_key("sub_button"):
				menu_button = {
					"name": menu_button['name'],
					"sub_button": []
				}
			doc = frappe.get_doc("Wechat Menu", sub_menu.menu)
			m = {
				"type": doc.menu_type or "view",
				"name": sub_menu.alias or doc.menu_name
			}
			if doc.route:
				url = "http://mm.symgrid.com/wechat/" + doc.route + "/" + app_name
			else:
				url = "http://mm.symgrid.com/wechat/home/" + app_name
			m["url"] = WeChatOAuth(app_id, secret, url).authorize_url
			menu_button["sub_button"].append(m)

		menu_buttons.append(menu_button)

	menu = {
		"button": menu_buttons
	}
	print(json.dumps(menu))
	client = WeChatClient(app_id, secret)
	client.menu.create(menu)
	print('--------------------------------------------------------')


def create_wechat_menu_2(app_name):
	print('--------------------------------------------------------')
	app_id = frappe.get_value('Wechat App', app_name, 'app_id')
	secret = frappe.get_value('Wechat App', app_name, 'secret')
	client = WeChatClient(app_id, secret)
	menu = {
		"button": [
			{
				"type": "view",
				"name": "主页",
				"url": "http://mm.symgrid.com/wechat/home/" + app_name
			},
			{
				"type": "view",
				"name": "我的设备",
				"url": "http://mm.symgrid.com/wechat/menu/" + app_name + "?menu=iot_devices"
			},
			{
				"name": "菜单",
				"sub_button": [
					{
						"type": "view",
						"name": "搜索",
						"url": "http://www.soso.com/"
					},
					{
						"type": "view",
						"name": "视频",
						"url": "http://v.qq.com/"
					},
					{
						"type": "click",
						"name": "赞一下我们",
						"key": "V1001_GOOD"
					}
				]
			}
		]
	}
	print(json.dumps(menu))
	client.menu.create(menu)
	print('--------------------------------------------------------')


@frappe.whitelist(allow_guest=True)
def wechat(app=None, signature=None, timestamp=None, nonce=None, encrypt_type='raw', msg_signature=None, echostr=None):
	app = app or 'test'
	TOKEN = frappe.get_value('Wechat App', app, 'token')

	try:
		check_signature(TOKEN, signature, timestamp, nonce)
	except InvalidSignatureException, e:
		return fire_raw_content(e, 403)

	if frappe.request.method == "GET":
		frappe.enqueue('wechat.api.create_wechat_menu', app_name=app)
		return fire_raw_content(echostr)

	# POST request
	if encrypt_type == 'raw':
		# plaintext mode
		msg = parse_message(frappe.form_dict.data)
		if msg.type == 'text':
			reply = create_reply(msg.content, msg)
		else:
			reply = create_reply('Sorry, can not handle this for now', msg)

		frappe.enqueue('wechat.api.create_wechat_menu', app_name=app)
		return fire_raw_content(reply.render(), 200, 'text/xml')
	else:
		# encryption mode
		from wechatpy.crypto import WeChatCrypto
		AES_KEY = frappe.get_value('Wechat App', app, 'aes_key')
		APP_ID = frappe.get_value('Wechat App', app, 'app_id')

		crypto = WeChatCrypto(TOKEN, AES_KEY, APP_ID)
		try:
			msg = crypto.decrypt_message(
				frappe.form_dict.data,
				msg_signature,
				timestamp,
				nonce
			)
		except (InvalidSignatureException, InvalidAppIdException), e:
			return fire_raw_content(e, 403)
		else:
			msg = parse_message(msg)
			if msg.type == 'text':
				reply = create_reply(msg.content, msg)
			else:
				reply = create_reply('Sorry, can not handle this for now', msg)
			frappe.enqueue('wechat.api.create_wechat_menu', app_name=app)
			return fire_raw_content(crypto.encrypt_message(reply.render(), nonce, timestamp), 200, 'text/xml')
