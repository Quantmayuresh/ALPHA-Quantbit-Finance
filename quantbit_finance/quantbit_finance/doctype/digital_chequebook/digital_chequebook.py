# Copyright (c) 2024, quantbit technologies pvt ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DigitalChequeBook(Document):

	def before_save(self):
		self.validating_active_status()
		self.creating_cheque_numbrs()
		

	def validating_active_status(self):
		length = len(self.get("chequebook" , filters = {'active': 1} ))
		if length > 1 :
			frappe.throw('Activation Status Must Be Unique')
		
		frappe.db.sql("update `tabChequebook Number details` set active_status = 0")
		series = self.get("chequebook" , filters = {'active': 1})
		for d in series:
			present_doc = frappe.get_all("Chequebook Number details", filters = {'cheque_series_reference':d.name , 'parent_document': self.name})
			for k in present_doc:
				frappe.db.sql("update `tabChequebook Number details` set active_status = 1 where name = %s",(k.name),)


	def creating_cheque_numbrs(self):
		for d in self.get("chequebook"):
			present = frappe.get_all("Chequebook Number details", filters = {'cheque_series_reference':d.name , 'cheque_number': d.cheque_no_from , 'parent_document': self.name})
			if not present:
				if d.cheque_no_from and d.cheque_no_to and d.cheque_no_from <= d.cheque_no_to :
					for i in range(d.cheque_no_from, d.cheque_no_to + 1):
						doc = frappe.new_doc("Chequebook Number details")
						doc.cheque_number = i
						doc.cheque_series_reference = d.name
						doc.account_no = self.bank_account_no
						doc.parent_type = 'Chequebook Number details'
						doc.parent_document = self.name
						doc.insert()
						doc.save()

						# self.append(
						# 		"Chequebook Number details",
						# 		{
						# 			"cheque_number": i,
						# 			"cheque_series_reference": d.name,
						# 			'account_no': self.bank_account_no ,
						# 		}
						# )

			

