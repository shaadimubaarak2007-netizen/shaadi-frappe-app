import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
		meta: { requiresAuth: false }
	},
	{
		name: "Login",
		path: "/signin",
		component: () => import("@/pages/Login.vue"),
		meta: { requiresAuth: false }
	},
	{
		name: "Signup",
		path: "/signup",
		component: () => import("@/pages/Signup.vue"),
		meta: { requiresAuth: false }
	},
	{
		path: "/login",
		redirect: "/signin"
	},
	{
		path: "/account/login",
		redirect: "/signin"
	},
	{
		path: "/dashboard",
		name: "Dashboard",
		component: () => import("@/pages/Dashboard.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/browse",
		name: "Browse",
		component: () => import("@/pages/Browse.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/profile/:id",
		name: "ProfileDetail",
		component: () => import("@/pages/ProfileDetail.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/my-profile",
		name: "MyProfile",
		component: () => import("@/pages/MyProfile.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/search",
		name: "Search",
		component: () => import("@/pages/Search.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/messages",
		name: "Messages",
		component: () => import("@/pages/Messages.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/matches",
		name: "Matches",
		component: () => import("@/pages/Matches.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/interests",
		name: "Interests",
		component: () => import("@/pages/Interests.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/shortlist",
		name: "Shortlist",
		component: () => import("@/pages/Shortlist.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/settings",
		name: "Settings",
		component: () => import("@/pages/Settings.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/subscription",
		name: "Subscription",
		component: () => import("@/pages/Subscription.vue"),
		meta: { requiresAuth: true }
	},
	{
		path: "/preferences",
		name: "PartnerPreferences",
		component: () => import("@/pages/PartnerPreferences.vue"),
		meta: { requiresAuth: true }
	}
]

const router = createRouter({
	history: createWebHistory("/"),
	routes,
})

router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

	const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

	if (to.name === "Login" && isLoggedIn) {
		next({ name: "Dashboard" })
	} else if (requiresAuth && !isLoggedIn) {
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router
