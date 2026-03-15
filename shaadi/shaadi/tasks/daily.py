import frappe
from frappe.utils import getdate, add_days


def expire_subscriptions():
	"""Mark expired subscriptions as expired and sync with Member Profile"""
	today = getdate()
	
	expired_subs = frappe.get_all(
		"Member Subscription",
		filters={
			"status": "Active",
			"end_date": ["<", today]
		},
		pluck="name"
	)
	
	for sub_name in expired_subs:
		try:
			sub = frappe.get_doc("Member Subscription", sub_name)
			sub.status = "Expired"
			# Save will trigger sync_to_member_profile() which handles Member Profile update
			sub.save(ignore_permissions=True)
			frappe.db.commit()
		except Exception as e:
			frappe.logger().error(f"Error expiring subscription {sub_name}: {str(e)}")
			frappe.db.rollback()
	
	if expired_subs:
		frappe.logger().info(f"Expired {len(expired_subs)} subscriptions")
	
	return len(expired_subs)


def send_match_digest():
	"""Send daily match digest to active members"""
	from shaadi.shaadi.utils.subscription import reset_daily_message_count
	
	# Reset daily message counts for all active subscriptions
	reset_daily_message_count()
	
	# Get all active members who want daily digest
	members = frappe.get_all(
		"Member Profile",
		filters={"is_active": 1},
		pluck="name"
	)
	
	for member in members:
		try:
			# Get top 5 matches from cache
			cache_key = f"top_matches:{member}"
			matches = frappe.cache().get_value(cache_key)
			
			if matches and len(matches) > 0:
				# Get member email
				member_email = frappe.db.get_value("Member Profile", member, "email")
				
				if member_email:
					# Send digest email
					send_daily_digest_email(member, member_email, matches[:5])
		except Exception as e:
			frappe.logger().error(f"Error sending digest to {member}: {str(e)}")
	
	frappe.logger().info(f"Sent match digest to {len(members)} members")


def send_daily_digest_email(profile_id, email, matches):
	"""Send daily match digest email"""
	try:
		from frappe.utils import get_url
		
		member_name = frappe.db.get_value("Member Profile", profile_id, "full_name")
		
		subject = _("Your Daily Match Recommendations")
		
		match_list = ""
		for match in matches:
			profile_data = frappe.db.get_value(
				"Member Profile",
				match["profile_id"],
				["full_name", "age", "city", "education"],
				as_dict=True
			)
			if profile_data:
				match_list += f"""
				<li>
					<strong>{profile_data.get('full_name')}</strong>, {profile_data.get('age')} years, {profile_data.get('city')}<br>
					{profile_data.get('education')}<br>
					Match Score: {match['score']}%
				</li>
				"""
		
		message = f"""
		<p>Dear {member_name},</p>
		
		<p>Here are your top match recommendations for today:</p>
		
		<ul>
		{match_list}
		</ul>
		
		<p><a href="{get_url()}/frontend/matches">View All Matches</a></p>
		
		<p>Best regards,<br>Shaadi Team</p>
		"""
		
		frappe.sendmail(
			recipients=[email],
			subject=subject,
			message=message,
			delayed=True
		)
	except Exception as e:
		frappe.logger().error(f"Error sending daily digest email: {str(e)}")


def precompute_matches():
	"""Precompute top matches for all active members (runs at 8 AM daily)"""
	from shaadi.shaadi.utils.match_score import get_top_matches
	
	members = frappe.get_all(
		"Member Profile",
		filters={"is_active": 1},
		pluck="name"
	)
	
	for member in members:
		try:
			matches = get_top_matches(member, limit=50)
			
			# Store in Redis cache for quick access
			cache_key = f"top_matches:{member}"
			frappe.cache().set_value(cache_key, matches, expires_in_sec=86400)  # 24 hours
			
		except Exception as e:
			frappe.logger().error(f"Error precomputing matches for {member}: {str(e)}")
	
	frappe.logger().info(f"Precomputed matches for {len(members)} members")
