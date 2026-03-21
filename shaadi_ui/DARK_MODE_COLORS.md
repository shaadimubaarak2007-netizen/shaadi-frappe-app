# Shaadi Dark Mode Color Mapping

## Replace Generic Grays with Shaadi Branded Colors

### Backgrounds
- `bg-gray-50` → `bg-shaadi-bg-base` (light) / stays as base in dark
- `bg-gray-950` → Use CSS variable `bg-shaadi-base` 
- `bg-white dark:bg-gray-900` → `bg-shaadi-surface`
- `bg-gray-100 dark:bg-gray-800` → `bg-shaadi-raised`

### Borders  
- `border-gray-200 dark:border-gray-800` → `border-shaadi`
- `border-gray-300 dark:border-gray-700` → `border-shaadi-mid`

### Text
- `text-gray-900 dark:text-white` → `text-shaadi-primary`
- `text-gray-600 dark:text-gray-400` → `text-shaadi-secondary`
- `text-gray-500 dark:text-gray-400` → `text-shaadi-tertiary`

### Skeleton/Loading States
- `bg-gray-200 dark:bg-gray-700` → `bg-gray-200 dark:bg-shaadi-dk-overlay`

### Specific Shaadi Colors (from tailwind.config.js)
- Dark backgrounds: `#0F0A0D` (dk-base), `#1A1115` (dk-surface), `#2A1820` (dk-raised)
- Dark borders: `#374151` (dk-border), `#4B5563` (dk-border-mid)
- Dark text: `#F9FAFB` (dk-ink), `#D1D5DB` (dk-body), `#9CA3AF` (dk-hint)
