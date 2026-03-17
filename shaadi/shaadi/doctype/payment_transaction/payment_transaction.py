# Copyright (c) 2024, Amit Kumar and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document


class PaymentTransaction(Document):
	def validate(self):
		"""Validate payment transaction before saving"""
		if not self.transaction_date:
			self.transaction_date = frappe.utils.now()
		
		if not self.currency:
			self.currency = "INR"
	
	def on_payment_authorized(self, payment_status):
		"""
		Called by Razorpay integration when payment is authorized/completed
		This method is called by the payments app after successful payment
		Following LMS pattern: Extract data from Integration Request
		"""
		try:
			frappe.logger().info(f"Payment authorized for {self.name}: {payment_status}")
			
			# Frontend URL for redirect
			frontend_url = "http://localhost:8080"
			
			if payment_status in ["Authorized", "Completed"]:
				# LMS pattern: Update payment record using Integration Request data
				# Note: update_payment_record handles saving the transaction
				update_payment_record(self.name)
				
				# Redirect to frontend Vue app with success status
				return f"{frontend_url}/subscription?payment=success&transaction={self.name}"
			else:
				# Reload to avoid timestamp mismatch
				txn = frappe.get_doc("Payment Transaction", self.name)
				txn.status = "Failed"
				txn.payment_status = payment_status
				txn.error_message = f"Payment status: {payment_status}"
				txn.save(ignore_permissions=True)
				frappe.db.commit()
				
				# Redirect to frontend Vue app with failure status
				return f"{frontend_url}/subscription?payment=failed&transaction={self.name}"
				
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Payment Authorization Error")
			# Reload to avoid timestamp mismatch
			txn = frappe.get_doc("Payment Transaction", self.name)
			txn.status = "Failed"
			txn.error_message = str(e)
			txn.save(ignore_permissions=True)
			frappe.db.commit()
			
			# Redirect to frontend Vue app with error status
			return f"{frontend_url}/subscription?payment=error&transaction={self.name}"
	
	def create_subscription(self):
		"""Create or update member subscription after successful payment"""
		try:
			from frappe.utils import add_days, getdate, today
			
			# Get subscription plan details
			plan = frappe.get_doc("Subscription Plan", self.subscription_plan)
			
			# STEP 1: Create/Update Subscription DocType (payment tracking)
			existing_subscription = frappe.db.get_value(
				"Subscription",
				{
					"member_profile": self.member_profile,
					"status": "Active"
				},
				["name", "end_date"],
				as_dict=True
			)
			
			if existing_subscription:
				# Extend existing subscription
				subscription_doc = frappe.get_doc("Subscription", existing_subscription.name)
				current_end = getdate(existing_subscription.end_date)
				new_end_date = add_days(current_end, plan.duration_days)
				subscription_doc.end_date = new_end_date
				subscription_doc.save(ignore_permissions=True)
				self.subscription = subscription_doc.name
			else:
				# Create new subscription
				subscription_doc = frappe.get_doc({
					"doctype": "Subscription",
					"member_profile": self.member_profile,
					"subscription_plan": self.subscription_plan,
					"start_date": today(),
					"end_date": add_days(today(), plan.duration_days),
					"status": "Active",
					"payment_transaction": self.name
				})
				subscription_doc.insert(ignore_permissions=True)
				self.subscription = subscription_doc.name
			
			# STEP 2: Create/Update Member Subscription DocType (usage tracking + Member Profile sync)
			existing_member_sub = frappe.db.get_value(
				"Member Subscription",
				{
					"member_profile": self.member_profile,
					"status": "Active"
				},
				["name", "end_date"],
				as_dict=True
			)
			
			if existing_member_sub:
				# Update existing Member Subscription
				member_sub_doc = frappe.get_doc("Member Subscription", existing_member_sub.name)
				
				# If upgrading to different plan, update plan
				if member_sub_doc.plan != self.subscription_plan:
					member_sub_doc.plan = self.subscription_plan
					member_sub_doc.start_date = today()
					member_sub_doc.end_date = add_days(today(), plan.duration_days)
					# Reset usage counters on plan change
					member_sub_doc.contacts_used = 0
					member_sub_doc.messages_today = 0
				else:
					# Same plan, extend end date
					current_end = getdate(existing_member_sub.end_date)
					member_sub_doc.end_date = add_days(current_end, plan.duration_days)
				
				# Update payment details
				member_sub_doc.amount_paid = self.amount
				member_sub_doc.razorpay_order_id = self.razorpay_order_id
				member_sub_doc.razorpay_payment_id = self.razorpay_payment_id
				member_sub_doc.razorpay_signature = self.razorpay_signature
				
				member_sub_doc.save(ignore_permissions=True)
				frappe.logger().info(f"Updated Member Subscription: {member_sub_doc.name}")
			else:
				# Create new Member Subscription
				member_sub_doc = frappe.get_doc({
					"doctype": "Member Subscription",
					"member_profile": self.member_profile,
					"plan": self.subscription_plan,
					"start_date": today(),
					"end_date": add_days(today(), plan.duration_days),
					"status": "Active",
					"amount_paid": self.amount,
					"razorpay_order_id": self.razorpay_order_id,
					"razorpay_payment_id": self.razorpay_payment_id,
					"razorpay_signature": self.razorpay_signature,
					"contacts_used": 0,
					"messages_today": 0
				})
				member_sub_doc.insert(ignore_permissions=True)
				frappe.logger().info(f"Created Member Subscription: {member_sub_doc.name}")
			
			self.save(ignore_permissions=True)
			frappe.db.commit()
			
			frappe.logger().info(f"Subscription created/updated: {self.subscription}")
			
		except Exception as e:
			frappe.log_error(frappe.get_traceback(), "Subscription Creation Error")
			raise


def update_payment_record(transaction_name):
	"""
	Update payment record after successful payment
	Following LMS pattern: Extract payment data from Integration Request
	
	Args:
		transaction_name: Payment Transaction name
	"""
	try:
		# Get latest Integration Request for this transaction (LMS pattern)
		request = frappe.get_all(
			"Integration Request",
			{
				"reference_doctype": "Payment Transaction",
				"reference_docname": transaction_name,
				"owner": frappe.session.user
			},
			order_by="creation desc",
			limit=1
		)
		
		if not request:
			frappe.log_error(f"No Integration Request found for {transaction_name}", "Payment Update Error")
			return
		
		# Extract payment data from Integration Request
		data = frappe.db.get_value("Integration Request", request[0].name, "data")
		data = frappe._dict(json.loads(data))
		
		# Determine payment ID field based on gateway (LMS pattern)
		payment_gateway = data.get("payment_gateway")
		if payment_gateway == "Razorpay":
			payment_id_field = "razorpay_payment_id"
		elif "Stripe" in payment_gateway:
			payment_id_field = "stripe_token_id"
		else:
			payment_id_field = "payment_id"
		
		# Update Payment Transaction record
		transaction = frappe.get_doc("Payment Transaction", transaction_name)
		transaction.status = "Completed"
		transaction.payment_status = "Completed"
		transaction.razorpay_payment_id = data.get(payment_id_field)
		transaction.razorpay_order_id = data.get("order_id")
		transaction.razorpay_signature = data.get("razorpay_signature")
		transaction.integration_request = request[0].name
		transaction.payment_response = json.dumps(data)
		transaction.save(ignore_permissions=True)
		
		# Create or update subscription
		transaction.create_subscription()
		
		frappe.db.commit()
		frappe.logger().info(f"Payment record updated for {transaction_name}")
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Update Payment Record Error")
		raise
