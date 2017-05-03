# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from wechatpy.oauth import WeChatOAuth
from wechat.api import check_wechat_binding


def is_webui_installed():
	return "sskl_webui" in frappe.get_installed_apps()


def get_context(context):
	context.no_cache = 1

	url = "/cell_station_map"
	if is_webui_installed():
		url = "/S_Station_Map"
	check_wechat_binding(redirect_url=url)
