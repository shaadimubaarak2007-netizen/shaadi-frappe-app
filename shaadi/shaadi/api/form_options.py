"""
API endpoints for fetching form field options from Frappe DocTypes
"""
import frappe

@frappe.whitelist(allow_guest=True)
def get_member_profile_options():
	"""
	Get all select field options for Member Profile DocType
	Returns options for: gender, religion, marital_status, education, occupation, state
	"""
	try:
		# Get Member Profile DocType meta
		meta = frappe.get_meta("Member Profile")
		
		options = {}
		
		# Fields to fetch options for
		fields_to_fetch = [
			"gender",
			"religion", 
			"marital_status",
			"education",
			"occupation",
			"state"
		]
		
		for fieldname in fields_to_fetch:
			field = meta.get_field(fieldname)
			if field and field.options:
				# Split options by newline and create label-value pairs
				field_options = []
				for option in field.options.split("\n"):
					option = option.strip()
					if option:
						field_options.append({
							"label": option,
							"value": option
						})
				options[fieldname] = field_options
		
		return options
		
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Get Member Profile Options Error")
		return {
			"error": str(e)
		}
