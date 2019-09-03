# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Wechat Messages"),
			"items": [
				{
					"type": "doctype",
					"name": "Wechat Send Doc",
					"onboard": 1,
					"description": _("Wechat Send Doc"),
				}
			]
		},
		{
			"label": _("Wechat Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "Wechat App",
					"onboard": 1,
					"description": _("Wechat App"),
				},
				{
					"type": "doctype",
					"name": "Wechat Homepage",
					"onboard": 1,
					"description": _("Wechat Homepage"),
				},
				{
					"type": "doctype",
					"name": "Wechat Binding",
					"onboard": 1,
					"description": _("Wechat Binding"),
				},
				{
					"type": "doctype",
					"name": "Wechat Menu",
					"onboard": 1,
					"description": _("Wechat Menu"),
				}
			]
		}
	]
