frappe.ready(function() {
	$(".btn-bind-wechat").click(function() {
		var args = {
			app: $("#app").val(),
			openid: $("#openid").val(),
			user: $("#login_email").val(),
			passwd: $("#login_password").val(),
		};

		if(!args.user) {
			frappe.msgprint("User Email Required.");
			return false;
		}

		frappe.call({
			type: "POST",
			method: "wechat.api.bind",
			btn: $(".btn-bind-wechat"),
			args: args,
			callback: function(r) {
				if(!r.exc) {
					$('.page-card-head .indicator').removeClass().addClass('indicator green')
						.html(__('Wechat Binding success'));
					if(r.message) {
						frappe.msgprint(__('Wechat Binding success'));
						setTimeout(function() {
							window.location.href = r.message;
						}, 2000);
					}
				} else {
					$('.page-card-head .indicator').removeClass().addClass('indicator red')
					.text(r.message);
				}
			}
		});

        return false;
	});
});