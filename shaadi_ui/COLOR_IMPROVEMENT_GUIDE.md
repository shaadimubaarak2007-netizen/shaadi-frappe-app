# Shaadi Dark Mode Color Improvement Guide

## Problem
Currently using generic Tailwind gray colors (`gray-900`, `gray-950`, `gray-800`) which don't align with the Shaadi brand's warm, romantic aesthetic.

## Solution
Use the Bandhan-inspired Shaadi color system with warm dark tones.

## Color Replacements

### Page Backgrounds
**Before:** `bg-gray-50 dark:bg-gray-950`
**After:** `bg-shaadi-base`
- Light: `#FDFAF5` (warm cream)
- Dark: `#0F0A0D` (warm deep black with pink undertone)

### Card/Surface Backgrounds
**Before:** `bg-white dark:bg-gray-900`
**After:** `bg-shaadi-surface`
- Light: `#FFFFFF`
- Dark: `#1A1115` (warm dark surface with subtle pink)

### Raised Elements
**Before:** `bg-gray-100 dark:bg-gray-800`
**After:** `bg-shaadi-raised`
- Light: `#F9FAFB`
- Dark: `#2A1820` (warm raised surface)

### Borders
**Before:** `border-gray-200 dark:border-gray-800`
**After:** `border-shaadi`
- Light: `#E5E7EB`
- Dark: `#374151`

**Before:** `border-gray-300 dark:border-gray-700`
**After:** `border-shaadi-mid`
- Light: `#D1D5DB`
- Dark: `#4B5563`

### Text Colors
**Before:** `text-gray-900 dark:text-white`
**After:** `text-shaadi-primary`
- Light: `#111827`
- Dark: `#F9FAFB`

**Before:** `text-gray-600 dark:text-gray-400`
**After:** `text-shaadi-secondary`
- Light: `#6B7280`
- Dark: `#D1D5DB`

**Before:** `text-gray-500 dark:text-gray-400`
**After:** `text-shaadi-tertiary`
- Light: `#9CA3AF`
- Dark: `#9CA3AF`

### Loading/Skeleton States
**Before:** `bg-gray-200 dark:bg-gray-700`
**After:** `bg-gray-200 dark:bg-shaadi-dk-overlay`
- Dark: `#33202A` (warm overlay)

## Benefits
1. **Brand Consistency**: Warm tones align with romantic/matrimonial theme
2. **Better Contrast**: Carefully chosen colors for readability
3. **Professional Look**: Cohesive color system throughout
4. **Accessibility**: Maintains WCAG contrast ratios
5. **CSS Variables**: Easy to adjust globally if needed
