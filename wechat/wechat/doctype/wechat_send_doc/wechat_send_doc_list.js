/**
 * Created by cch on 17-3-16.
 */
frappe.listview_settings['Wechat Send Doc'] = {
	get_indicator: function(doc) {
		colour = {'New': 'blue', 'Partial': 'orange', 'Finished': 'green', 'Error': 'red'};
		return [__(doc.status), colour[doc.status], "status,=," + doc.status];
	},
	onload: function(me) {
		frappe.route_options = {
			"status": ['in', "New,Partial,Error"]
		};
	},
	add_fields: ["document_type", "document_id"],
}
