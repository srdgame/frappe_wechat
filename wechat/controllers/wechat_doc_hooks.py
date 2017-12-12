# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import format_datetime


def todo_tmsg_data(doc, method):
	return {
		"first": {
			"value": _("You have new ToDo"),
			"color": "#800000"
		},
		"keyword1": {
			"value": doc.priority,
			"color": "#000080"
		},
		"keyword2": {
			"value": doc.assigned_by_full_name,
			"color": "#000080"
		},
		"keyword3": {
			"value": format_datetime(doc.date),  # 时间
			"color": "#008000",
		},
		"remark": {
			"value": _("详情: {0}").format(doc.description)
		}
	}


def todo_tmsg_url(doc, method):
	return doc.get_url()