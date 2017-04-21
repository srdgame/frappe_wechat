# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from wechat.api import check_wechat_binding


def get_context(context):
	context.no_cache = 1

	check_wechat_binding(redirect_url="/cell_station_list")
