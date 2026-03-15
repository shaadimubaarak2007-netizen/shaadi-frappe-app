import { createApp } from "vue"
import { FrappeUI } from "frappe-ui"

import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"
import "./index.css"

import {
	Alert,
	Badge,
	Button,
	Card,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	TextInput,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
} from "frappe-ui"

const globalComponents = {
	Button,
	Card,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
}

const app = createApp(App)

setConfig("resourceFetcher", frappeRequest)

app.use(router)
app.use(resourcesPlugin)
app.use(pageMetaPlugin)

const socket = initSocket()
app.config.globalProperties.$socket = socket

for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

app.mount("#app")
