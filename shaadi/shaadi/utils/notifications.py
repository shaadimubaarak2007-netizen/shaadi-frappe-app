import frappe
from frappe import _
from frappe.utils import get_url


def on_profile_created(doc, method):
	"""Send welcome notification when profile is created"""
	frappe.logger().info(f"Profile created: {doc.name}")
	send_welcome_email(doc)


def on_profile_updated(doc, method):
	"""Handle profile updates"""
	if doc.has_value_changed("verified") and doc.verified:
		frappe.logger().info(f"Profile verified: {doc.name}")
		send_verification_email(doc)


def on_interest_response(doc, method):
	"""Notify when interest is accepted/declined"""
	if doc.has_value_changed("status"):
		if doc.status == "Accepted":
			frappe.logger().info(f"Interest accepted: {doc.name}")
			send_interest_accepted_notification(doc)
		elif doc.status == "Declined":
			frappe.logger().info(f"Interest declined: {doc.name}")
			send_interest_declined_notification(doc)


def on_new_message(doc, method):
	"""Notify receiver of new message"""
	conversation = frappe.get_doc("Conversation", doc.conversation)
	
	# Determine receiver
	receiver = conversation.participant_2 if doc.sender == conversation.participant_1 else conversation.participant_1
	
	frappe.logger().info(f"New message from {doc.sender} to {receiver}")
	send_new_message_notification(doc, receiver)


# Email notification functions

def send_welcome_email(profile_doc):
	"""Send welcome email to new member"""
	try:
		user_email = profile_doc.email
		
		if not user_email:
			return
		
		subject = _("Welcome to Shaadi - Complete Your Profile")
		
		message = f"""
		<p>Dear {profile_doc.full_name},</p>
		
		<p>Welcome to Shaadi! We're excited to have you join our matrimonial platform.</p>
		
		<p>To get the best matches, please complete your profile with the following information:</p>
		<ul>
			<li>Upload your profile photo</li>
			<li>Add your education and occupation details</li>
			<li>Fill in your partner preferences</li>
			<li>Add family details</li>
		</ul>
		
		<p>Your profile is currently {profile_doc.profile_completeness}% complete.</p>
		
		<p><a href="{get_url()}/frontend/profile">Complete Your Profile</a></p>
		
		<p>Best regards,<br>Shaadi Team</p>
		"""
		
		frappe.sendmail(
			recipients=[user_email],
			subject=subject,
			message=message,
			delayed=False
		)
		
		frappe.logger().info(f"Welcome email sent to {user_email}")
	except Exception as e:
		frappe.logger().error(f"Error sending welcome email: {str(e)}")


def send_verification_email(profile_doc):
	"""Send verification success email"""
	try:
		user_email = profile_doc.email
		
		if not user_email:
			return
		
		subject = _("Your Profile Has Been Verified!")
		
		message = f"""
		<p>Dear {profile_doc.full_name},</p>
		
		<p>Congratulations! Your profile has been verified by our team.</p>
		
		<p>Verified profiles get:</p>
		<ul>
			<li>Higher visibility in search results</li>
			<li>More trust from other members</li>
			<li>Better match recommendations</li>
		</ul>
		
		<p><a href="{get_url()}/frontend/matches">View Your Matches</a></p>
		
		<p>Best regards,<br>Shaadi Team</p>
		"""
		
		frappe.sendmail(
			recipients=[user_email],
			subject=subject,
			message=message,
			delayed=False
		)
		
		frappe.logger().info(f"Verification email sent to {user_email}")
	except Exception as e:
		frappe.logger().error(f"Error sending verification email: {str(e)}")


def send_interest_accepted_notification(match_request_doc):
	"""Notify sender that their interest was accepted"""
	try:
		sender_email = frappe.db.get_value("Member Profile", match_request_doc.sender, "email")
		receiver_name = frappe.db.get_value("Member Profile", match_request_doc.receiver, "full_name")
		
		if not sender_email:
			return
		
		subject = _("Your Interest Was Accepted!")
		
		message = f"""
		<p>Great news!</p>
		
		<p>{receiver_name} has accepted your interest.</p>
		
		<p>You can now start a conversation and get to know each other better.</p>
		
		<p><a href="{get_url()}/frontend/conversations">Start Conversation</a></p>
		
		<p>Best regards,<br>Shaadi Team</p>
		"""
		
		frappe.sendmail(
			recipients=[sender_email],
			subject=subject,
			message=message,
			delayed=False
		)
		
		frappe.logger().info(f"Interest accepted notification sent to {sender_email}")
	except Exception as e:
		frappe.logger().error(f"Error sending interest accepted notification: {str(e)}")


def send_interest_declined_notification(match_request_doc):
	"""Notify sender that their interest was declined"""
	try:
		sender_email = frappe.db.get_value("Member Profile", match_request_doc.sender, "email")
		
		if not sender_email:
			return
		
		subject = _("Interest Update")
		
		message = f"""
		<p>Thank you for your interest.</p>
		
		<p>Unfortunately, the member you expressed interest in has declined at this time.</p>
		
		<p>Don't worry! There are many other compatible matches waiting for you.</p>
		
		<p><a href="{get_url()}/frontend/matches">View More Matches</a></p>
		
		<p>Best regards,<br>Shaadi Team</p>
		"""
		
		frappe.sendmail(
			recipients=[sender_email],
			subject=subject,
			message=message,
			delayed=False
		)
		
		frappe.logger().info(f"Interest declined notification sent to {sender_email}")
	except Exception as e:
		frappe.logger().error(f"Error sending interest declined notification: {str(e)}")


def send_new_message_notification(message_doc, receiver_profile_id):
	"""Send email notification for new message"""
	try:
		receiver_email = frappe.db.get_value("Member Profile", receiver_profile_id, "email")
		sender_name = frappe.db.get_value("Member Profile", message_doc.sender, "full_name")
		
		if not receiver_email:
			return
		
		subject = _("New Message from {0}").format(sender_name)
		
		message_preview = message_doc.message_text[:100] + "..." if len(message_doc.message_text) > 100 else message_doc.message_text
		
		message = f"""
		<p>You have a new message from {sender_name}:</p>
		
		<blockquote>{message_preview}</blockquote>
		
		<p><a href="{get_url()}/frontend/conversations/{message_doc.conversation}">View Conversation</a></p>
		
		<p>Best regards,<br>Shaadi Team</p>
		"""
		
		frappe.sendmail(
			recipients=[receiver_email],
			subject=subject,
			message=message,
			delayed=False
		)
		
		frappe.logger().info(f"New message notification sent to {receiver_email}")
	except Exception as e:
		frappe.logger().error(f"Error sending new message notification: {str(e)}")


# SMS notification functions (using MSG91 or Twilio)

def send_otp_sms(phone, otp):
	"""Send OTP via SMS"""
	try:
		# TODO: Integrate with MSG91 or Twilio
		# For now, just log
		frappe.logger().info(f"OTP SMS to {phone}: {otp}")
		
		# Example MSG91 integration:
		# import requests
		# url = "https://api.msg91.com/api/v5/otp"
		# payload = {
		#     "template_id": "YOUR_TEMPLATE_ID",
		#     "mobile": phone,
		#     "otp": otp
		# }
		# headers = {"authkey": "YOUR_AUTH_KEY"}
		# response = requests.post(url, json=payload, headers=headers)
		
		return True
	except Exception as e:
		frappe.logger().error(f"Error sending OTP SMS: {str(e)}")
		return False


def send_match_notification_sms(phone, match_name):
	"""Send SMS notification for new match"""
	try:
		# TODO: Integrate with SMS gateway
		frappe.logger().info(f"Match notification SMS to {phone}: New match with {match_name}")
		return True
	except Exception as e:
		frappe.logger().error(f"Error sending match notification SMS: {str(e)}")
		return False
