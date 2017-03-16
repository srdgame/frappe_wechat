/**
 * Created by cch on 17-3-16.
 */
frappe.listview_settings['Wechat Send Soc'] = {
	get_indicator: function(doc) {
		colour = {'New': 'red', 'Partial': 'orange', 'Finished': 'green'};
		return [__(doc.status), colour[doc.status], "status,=," + doc.status];
	},
	onload: function(me) {
		frappe.route_options = {
			"status": ['in', "New,Partial"]
		};
	},
	add_fields: ["doc_type", "doc_id"],
}
