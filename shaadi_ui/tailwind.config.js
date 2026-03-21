module.exports = {
	content: [
		"./index.html",
		"./src/**/*.{vue,js,ts,jsx,tsx}",
		"./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
		"../node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
	],
	darkMode: 'class',
	theme: {
		extend: {
			colors: {
				shaadi: {
					// Primary brand colors
					pink: {
						50: '#FDF0F3',
						100: '#FCE7F3',
						200: '#FBCFE8',
						400: '#F472B6',
						DEFAULT: '#EC4899',
						600: '#DB2777',
						700: '#BE185D',
						dark: '#F472B6',
						muted: '#3D1828',
					},
					purple: {
						50: '#FAF5FF',
						100: '#F3E8FF',
						200: '#E9D5FF',
						400: '#C084FC',
						DEFAULT: '#A855F7',
						600: '#9333EA',
						700: '#7E22CE',
						dark: '#C084FC',
						muted: '#2E1065',
					},
					// Background colors
					bg: {
						base: '#FDFAF5',
						surface: '#FFFFFF',
						raised: '#F9FAFB',
						overlay: '#F3F4F6',
					},
					// Dark backgrounds
					'dk-base': '#0F0A0D',
					'dk-surface': '#1A1115',
					'dk-raised': '#2A1820',
					'dk-overlay': '#33202A',
					// Text colors
					ink: '#111827',
					body: '#6B7280',
					hint: '#9CA3AF',
					'dk-ink': '#F9FAFB',
					'dk-body': '#D1D5DB',
					'dk-hint': '#9CA3AF',
					// Borders
					border: '#E5E7EB',
					'border-mid': '#D1D5DB',
					'dk-border': '#374151',
					'dk-border-mid': '#4B5563',
				},
			},
			borderRadius: {
				'shaadi-sm': '6px',
				'shaadi-md': '10px',
				'shaadi-lg': '14px',
				'shaadi-xl': '20px',
			},
			borderWidth: {
				'shaadi': '0.5px',
			},
		},
	},
	plugins: [],
}
