/**
 * Created by cch on 17-4-20.
 */
frappe.ready(function() {
	setTimeout(function() {
			window.location.href = "{{ redirect_location }}";
	}, 50);
}