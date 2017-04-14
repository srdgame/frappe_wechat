// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wechat Menu', {
	refresh: function(frm) {
		frappe.call({
			type: 'GET',
			method: "wechat.wechat.doctype.wechat_menu.wechat_menu.query_menu_routes",
			callback: function (r, rt) {
				if (r.message) {
					frm.set_df_property('route', 'options', r.message);
				}
			}
		});
	}
});
