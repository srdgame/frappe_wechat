/**
 * Created by cch on 17-3-16.
 */
frappe.listview_settings['Wechat Send Doc'] = {
	onload: function(me) {
		if (!frappe.route_options) {
			frappe.route_options = {
				"status": ['in', "New,Partial,Error"]
			};
		}
	},
	get_indicator: function(doc) {
		if(doc.status == "New") {
			return [__("New"), "bue"];
		}else if(doc.status == "Partial") {
			return [__("Partial"), "orange"];
		} else if(doc.status == "Finished") {
			return [__("Finished"), "green"];
		} else if(doc.status == "Error") {
			return [__("Error"), "red"];
		}
	},
	add_fields: ["document_type", "document_id"],
};
