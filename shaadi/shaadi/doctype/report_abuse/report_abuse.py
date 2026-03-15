import frappe
from frappe.model.document import Document


class ReportAbuse(Document):
	def on_submit(self):
		"""Notify moderators about new abuse report"""
		# Create notification for moderators
		moderators = frappe.get_all("User", filters={"role": "Matrimonial Moderator"}, pluck="name")
		for moderator in moderators:
			frappe.get_doc({
				"doctype": "Notification",
				"recipient": moderator,
				"notification_type": "System",
				"title": "New Abuse Report",
				"message": f"Profile {self.reported_profile} has been reported for {self.reason}",
				"link": f"/app/report-abuse/{self.name}"
			}).insert(ignore_permissions=True)
