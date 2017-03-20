# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import format_datetime


def todo_tmsg_data(doc, method):
	return {
		"first": {
			"value": _("You have new ToDo"),
			"color": "red"
		},
		"keyword1": {
			"value": doc.priority,
			"color": "blue"
		},
		"keyword2": {
			"value": doc.assigned_by_full_name,
			"color": "blue"
		},
		"keyword3": {
			"value": format_datetime(doc.date),  # 时间
			"color": "green",
		},
		"remark": {
			"value": _("详情: {0}").format(doc.description)
		}
	}


def todo_tmsg_url(doc, method):
	return doc.get_url()