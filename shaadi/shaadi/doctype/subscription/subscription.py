# Copyright (c) 2024, Amit Kumar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class Subscription(Document):
	def validate(self):
		"""Validate subscription before saving"""
		# Ensure start date is not after end date
		if self.start_date and self.end_date:
			if getdate(self.start_date) > getdate(self.end_date):
				frappe.throw("Start date cannot be after end date")
		
		# Auto-update status based on dates
		self.update_status()
		
		# Store plan details for reference
		if self.subscription_plan and not self.plan_details:
			plan = frappe.get_doc("Subscription Plan", self.subscription_plan)
			price = plan.price_inr or plan.price or 0
			self.plan_details = f"{plan.plan_name} - ₹{price} for {plan.duration_days} days"
	
	def update_status(self):
		"""Update subscription status based on dates"""
		if not self.end_date:
			return
		
		current_date = getdate(today())
		end_date = getdate(self.end_date)
		
		# Only auto-update if currently Active
		if self.status == "Active" and current_date > end_date:
			self.status = "Expired"
	
	def on_update(self):
		"""After subscription is updated"""
		# Update member profile with active subscription plan
		if self.status == "Active":
			# Update subscription_plan field in Member Profile
			frappe.db.set_value(
				"Member Profile",
				self.member_profile,
				"subscription_plan",
				self.subscription_plan
			)
			
			# Set featured flag if plan includes it
			plan = frappe.get_doc("Subscription Plan", self.subscription_plan)
			if plan.featured_profile:
				frappe.db.set_value("Member Profile", self.member_profile, "featured", 1)
			
			frappe.logger().info(f"Updated Member Profile {self.member_profile} with plan {self.subscription_plan}")
			
		elif self.status in ["Expired", "Cancelled"]:
			# Check if there are any other active subscriptions
			other_active = frappe.db.exists(
				"Subscription",
				{
					"member_profile": self.member_profile,
					"status": "Active",
					"name": ["!=", self.name]
				}
			)
			
			if not other_active:
				# No other active subscriptions, revert to Free plan
				frappe.db.set_value("Member Profile", self.member_profile, "subscription_plan", "Free")
				frappe.db.set_value("Member Profile", self.member_profile, "featured", 0)
				frappe.logger().info(f"Reverted Member Profile {self.member_profile} to Free plan")
