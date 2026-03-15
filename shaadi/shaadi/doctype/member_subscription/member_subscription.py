import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate, nowdate
from frappe import _


class MemberSubscription(Document):
	def validate(self):
		"""Validate subscription before saving"""
		# Check for duplicate active subscriptions
		if self.status == "Active":
			existing = frappe.db.get_value(
				"Member Subscription",
				{
					"member_profile": self.member_profile,
					"status": "Active",
					"name": ["!=", self.name]
				}
			)
			if existing:
				frappe.throw(_("Member already has an active subscription. Please cancel or expire the existing subscription first."))
		
		# Validate dates
		if self.start_date and self.end_date:
			if getdate(self.end_date) < getdate(self.start_date):
				frappe.throw(_("End date cannot be before start date"))
		
		# Auto-expire if end date has passed
		if self.status == "Active" and self.end_date:
			if getdate(self.end_date) < getdate(nowdate()):
				self.status = "Expired"
	
	def before_save(self):
		"""Set default dates based on plan"""
		if not self.start_date:
			self.start_date = getdate()
		
		if self.start_date and not self.end_date:
			plan = frappe.get_doc("Subscription Plan", self.plan)
			if plan.duration_days:
				self.end_date = add_days(self.start_date, plan.duration_days)
	
	def on_update(self):
		"""Sync subscription status with Member Profile"""
		self.sync_to_member_profile()
	
	def on_trash(self):
		"""Handle subscription deletion"""
		if self.status == "Active":
			# Reset member profile to Free plan
			frappe.db.set_value("Member Profile", self.member_profile, "subscription_plan", "Free")
			frappe.db.set_value("Member Profile", self.member_profile, "featured", 0)
	
	def sync_to_member_profile(self):
		"""Sync subscription data to Member Profile"""
		if self.status == "Active":
			# Update Member Profile with active subscription plan
			frappe.db.set_value("Member Profile", self.member_profile, "subscription_plan", self.plan)
			
			# Set featured flag if plan includes it
			plan = frappe.get_doc("Subscription Plan", self.plan)
			if plan.featured_profile:
				frappe.db.set_value("Member Profile", self.member_profile, "featured", 1)
			else:
				frappe.db.set_value("Member Profile", self.member_profile, "featured", 0)
			
			# Deactivate any other active subscriptions for this member
			other_active = frappe.get_all(
				"Member Subscription",
				filters={
					"member_profile": self.member_profile,
					"status": "Active",
					"name": ["!=", self.name]
				}
			)
			for sub in other_active:
				frappe.db.set_value("Member Subscription", sub.name, "status", "Cancelled")
			
		elif self.status in ["Expired", "Cancelled", "Refunded"]:
			# Check if there are any other active subscriptions
			other_active = frappe.db.get_value(
				"Member Subscription",
				{
					"member_profile": self.member_profile,
					"status": "Active",
					"name": ["!=", self.name]
				},
				"plan"
			)
			
			if not other_active:
				# No other active subscriptions, set to Free plan
				frappe.db.set_value("Member Profile", self.member_profile, "subscription_plan", "Free")
				frappe.db.set_value("Member Profile", self.member_profile, "featured", 0)
