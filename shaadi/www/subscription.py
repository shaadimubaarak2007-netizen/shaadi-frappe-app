import frappe

def get_context(context):
	"""Serve the Vue app for /subscription route"""
	# This prevents Frappe from treating 'subscription' as a DocType list
	# The Vue app will handle the actual /subscription page rendering
	context.no_cache = 1
	return context
