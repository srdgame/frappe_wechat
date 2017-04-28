// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wechat App', {
	refresh: function(frm) {
		if (frappe.user.has_role(['Administrator', 'Wechat Manager', 'Company Admin'])){
			frm.add_custom_button(__("Update Wechat Menu"), function() {
				 	frappe.call({
						doc: frm.doc,
						method: "update_menu",
						freeze: true,
						callback: function(r)  {
							if(r.exc) {
								if(r._server_messages)
									frappe.msgprint(r._server_messages);
							} else {
								frappe.msgprint(__("Update WeChat Menu Successfully"));
							}
						}
					})
			}).removeClass("btn-default").addClass("btn-primary");
		}
	}
});
