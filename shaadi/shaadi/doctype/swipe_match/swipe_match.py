import frappe
from frappe.model.document import Document


class SwipeMatch(Document):
	def before_insert(self):
		"""Set created_on timestamp and check for mutual match"""
		self.created_on = frappe.utils.now()
		
		# Calculate match score if not provided
		if not self.match_score and self.action == "Like":
			from shaadi.shaadi.utils.match_score import calculate_match_score
			self.match_score = calculate_match_score(self.swiper, self.swiped_profile)
	
	def after_insert(self):
		"""Check for mutual match after creating swipe record"""
		if self.action == "Like":
			self.check_mutual_match()
	
	def check_mutual_match(self):
		"""Check if both users have liked each other"""
		# Look for reverse swipe (swiped_profile liked swiper)
		mutual_swipe = frappe.db.exists("Swipe Match", {
			"swiper": self.swiped_profile,
			"swiped_profile": self.swiper,
			"action": "Like"
		})
		
		if mutual_swipe:
			# Update both records to mark as mutual
			mutual_match_date = frappe.utils.now()
			
			# Update current record
			frappe.db.set_value("Swipe Match", self.name, {
				"is_mutual": 1,
				"mutual_match_date": mutual_match_date
			})
			
			# Update the reverse record
			frappe.db.set_value("Swipe Match", mutual_swipe, {
				"is_mutual": 1,
				"mutual_match_date": mutual_match_date
			})
			
			# Publish real-time event for mutual match
			frappe.publish_realtime("mutual_match", {
				"user1": self.swiper,
				"user2": self.swiped_profile,
				"match_date": mutual_match_date
			}, user=self.swiper)
			
			frappe.publish_realtime("mutual_match", {
				"user1": self.swiped_profile,
				"user2": self.swiper,
				"match_date": mutual_match_date
			}, user=self.swiped_profile)
			
			frappe.db.commit()
			
			return True
		
		return False
