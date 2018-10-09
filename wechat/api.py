# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import uuid
from frappe import throw, msgprint, _
from frappe.utils import get_fullname
from wechat.doctype.wechat_binding.wechat_binding import wechat_bind, wechat_unbind
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from wechatpy import WeChatClient
from wechatpy.oauth import WeChatOAuth


def check_wechat_binding(app=None, redirect_url=None):
	app = app or frappe.form_dict.app

	code = frappe.form_dict.code

	app_id = frappe.get_value('Wechat App', app, 'app_id')
	secret = frappe.get_value('Wechat App', app, 'secret')

	auth = WeChatOAuth(app_id, secret, '')
	token = auth.fetch_access_token(code)
	openid = token["openid"]
	expires_in = token['expires_in']

	user = frappe.get_value('Wechat Binding', {'app': app, 'openid': openid}, 'user')
	if not user:
		redirect = "/" #redirect_url or frappe.form_dict.redirect or ('wechat/home/' + app)
		url = "/wechat_login?app=" + app + "&openid=" + openid + "&redirect=" + redirect
		frappe.local.flags.redirect_location = url
		raise frappe.Redirect

	frappe.logger(__name__).info(_("check_wechat_binding {0} {1}").format(frappe.session.user, user))
	if frappe.session.user != user:
		#frappe.local.login_manager.clear_cookies()
		frappe.local.cookie_manager.to_delete = []
		frappe.local.login_manager.login_as(user)

	if redirect_url:
		#frappe.local.response["type"] = "redirect"
		#frappe.local.response["location"] = redirect_url
		frappe.local.flags.redirect_location = redirect_url
		frappe.local.response["home_page"] = redirect_url
		frappe.local.response["redirect_to"] = redirect_url
		raise frappe.Redirect
	else:
		return app


@frappe.whitelist()
def send_wechat_msg(app, users, msg):
	enable = frappe.get_value('Wechat App', app, "enabled")
	if not enable:
		throw(_("wechat not existed or disabled!"))

	ids = [d[0] for d in frappe.db.get_values('Wechat Binding', {"app": app, "user": ["in", users]}, "openid")]
	print("Wechat sending notify : {0} to openids {1} via app {2}".format(msg, ids, app))


def send_doc(app, doc_type, doc_id, users, msg_type='Template'):
	data = {
		"app": app,
		"document_type": doc_type,
		"document_id": doc_id,
		"type": msg_type,
	}
	data.update({
		"doctype": "Wechat Send Doc"
	})
	doc = frappe.get_doc(data)
	for user in users:
		doc.append("to_users", {
			"user": user,
			"sent": 0,
			"status": 'New',
		})
	doc = doc.insert()
	doc.submit()
	return doc.as_dict()


def clean_doc(doc_type, doc_id):
	for d in frappe.db.get_values("Wechat Send Doc", {"document_type": doc_type, "document_id": doc_id}, "name"):
		frappe.delete_doc("Wechat Send Doc", d[0])


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
	redirect = redirect or "/"
	if not (app and openid and user and passwd):
		return fire_raw_content("App, OpenID, User, Passwd is required!", 403)

	frappe.local.login_manager.authenticate(user, passwd)
	if frappe.local.login_manager.user != user:
		throw(_("Username password is not matched!"))

	frappe.local.login_manager.user = user
	frappe.local.login_manager.post_login()

	wechat_bind(app, user, openid, expires)

	#if redirect:
	#	frappe.local.response["type"] = "redirect"
	#	frappe.local.response["location"] = redirect if frappe.local.response.get('message') == 'Logged In' else "/"

	return redirect or _("Wechat binded!")


@frappe.whitelist(allow_guest=True)
def check_bind(app, openid, gen_token=False):
	if frappe.request.method != "POST" and frappe.request.method != "PUT":
		throw(_("Request Method Must be POST!"))

	from iot.user_api import valid_auth_code
	valid_auth_code()

	frappe.logger(__name__).info(_("check_bind {0}").format(openid))

	user = frappe.get_value('Wechat Binding', {'app': app, 'openid': openid}, 'user')
	if not user:
		throw(_("Openid is not bind with any user"))

	token = frappe.get_value("IOT User Api", user, 'authorization_code')

	if not token and gen_token is not False:
		doc = frappe.get_doc({
			"doctype": "IOT User Api",
			"user": user,
			"authorization_code": str(uuid.uuid1()).upper()
		}).insert()

		token = doc.authorization_code

	return {
		"user": user,
		"fullname": get_fullname(user),
		"token": token
	}


def create_wechat_menu(app_name):
	print('--------------------------------------------------------')
	app_id = frappe.get_value('Wechat App', app_name, 'app_id')
	secret = frappe.get_value('Wechat App', app_name, 'secret')
	domain = "http://" + (frappe.get_value('Wechat App', app_name, 'domain') or "mm.symgrid.com")

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
			url = domain + "/wechat/" + doc.route + "/" + app_name
		else:
			url = domain + "/wechat/home/" + app_name
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
				url = domain + "/wechat/" + doc.route + "/" + app_name
			else:
				url = domain + "/wechat/home/" + app_name
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


@frappe.whitelist(allow_guest=True, xss_safe=True)
def wechat(app=None, signature=None, timestamp=None, nonce=None, encrypt_type='raw', msg_signature=None, echostr=None):
	"""
	微信回调接口
	:param app: 
	:param signature: 
	:param timestamp: 
	:param nonce: 
	:param encrypt_type: 
	:param msg_signature: 
	:param echostr: 
	:return: 
	"""
	app = app or 'test'
	TOKEN = frappe.get_value('Wechat App', app, 'token')

	try:
		check_signature(TOKEN, signature, timestamp, nonce)
	except InvalidSignatureException, e:
		return fire_raw_content(e, 403)

	if frappe.request.method == "GET":
		#frappe.enqueue('wechat.api.create_wechat_menu', app_name=app)
		return fire_raw_content(echostr)

	#data = frappe.request.get_data()
	data = frappe.form_dict.data.decode('utf-8')
	frappe.logger(__name__).info(_("Received WeChat message {0}").format(data))

	# POST request
	if encrypt_type == 'raw':
		# plaintext mode
		msg = parse_message(data)
		if msg.type == 'text':
			reply = create_reply(msg.content, msg)
		else:
			reply = create_reply(_('Welcome to follow our WeChat Official Accounts'), msg)

		return fire_raw_content(reply.render(), 200, 'text/xml')
	else:
		# encryption mode
		from wechatpy.crypto import WeChatCrypto
		AES_KEY = frappe.get_value('Wechat App', app, 'aes_key')
		APP_ID = frappe.get_value('Wechat App', app, 'app_id')

		crypto = WeChatCrypto(TOKEN, AES_KEY, APP_ID)
		try:
			msg = crypto.decrypt_message(
				data,
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
				reply = create_reply(_('Welcome to follow our WeChat Official Accounts'), msg)
			#frappe.enqueue('wechat.api.create_wechat_menu', app_name=app)
			return fire_raw_content(crypto.encrypt_message(reply.render(), nonce, timestamp), 200, 'text/xml')
