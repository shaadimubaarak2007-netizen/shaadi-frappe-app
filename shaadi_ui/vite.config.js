import path from "path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue(),
		frappeui({
			buildConfig: {
				indexHtmlPath: path.resolve(__dirname, 'index.html')
			}
		})
	],
	build: {
		outDir: "../shaadi/public",
		emptyOutDir: true,
		target: "es2015",
		commonjsOptions: {
			include: [/tailwind.config.js/, /node_modules/],
		},
		sourcemap: true,
		rollupOptions: {
			output: {
				manualChunks: {
					"frappe-ui": ["frappe-ui"],
				},
			},
		},
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
		},
	},
	optimizeDeps: {
		include: [
			"frappe-ui > feather-icons",
			"showdown",
			"tailwind.config.js",
			"engine.io-client",
		],
	},
	server: {
		port: 8080,
		proxy: {
			"^/(app|login|api|assets|files|private)": {
				target: "http://localhost:8000",
				ws: true,
				router: function (req) {
					const site_name = req.headers.host.split(":")[0]
					return `http://${site_name}:8000`
				},
			},
		},
	},
})
