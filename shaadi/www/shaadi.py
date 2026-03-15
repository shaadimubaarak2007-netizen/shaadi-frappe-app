import frappe
from frappe.boot import load_translations

no_cache = 1

def get_context(context):
	"""
	Context for Shaadi frontend web page following HRMS/Ascra pattern
	"""
	csrf_token = frappe.sessions.get_csrf_token()
	frappe.db.commit()  # nosempgrep
	
	context.csrf_token = csrf_token
	context.site_name = frappe.local.site
	context.boot = get_boot()
	context.no_cache = 1
	context.show_sidebar = False
	context.title = "Shaadi - Matrimonial Platform"

@frappe.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
	if not frappe.conf.developer_mode:
		frappe.throw(frappe._("This method is only meant for developer mode"))
	return get_boot()

def get_boot():
	bootinfo = frappe._dict(
		{
			"site_name": frappe.local.site,
			"push_relay_server_url": frappe.conf.get("push_relay_server_url") or "",
			"default_route": get_default_route(),
		}
	)

	bootinfo.lang = frappe.local.lang
	load_translations(bootinfo)

	return bootinfo

def get_default_route():
	return "/"
