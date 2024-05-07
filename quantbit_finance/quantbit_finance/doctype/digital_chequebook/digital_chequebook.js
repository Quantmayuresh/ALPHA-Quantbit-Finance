// Copyright (c) 2024, quantbit technologies pvt ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Digital ChequeBook', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Digital ChequeBook', {
	setup: function(frm) {
        frm.set_query("bank_account", function(doc) {
            return {
                filters: [
                    ['Bank Account', 'is_company_account', '=', 1]
                ]
            };
        });
    }
});