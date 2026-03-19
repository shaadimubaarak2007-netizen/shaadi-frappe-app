import { ref, computed, watch } from 'vue'
import { useStorage } from '@vueuse/core'

const colorMode = useStorage('shaadi-color-mode', 'light')
const primaryColor = useStorage('shaadi-primary-color', 'pink')

const colors = {
  pink: {
    name: 'Pink',
    light: '#EC4899',
    dark: '#F472B6'
  },
  purple: {
    name: 'Purple',
    light: '#9333EA',
    dark: '#A855F7'
  },
  rose: {
    name: 'Rose',
    light: '#F43F5E',
    dark: '#FB7185'
  },
  fuchsia: {
    name: 'Fuchsia',
    light: '#D946EF',
    dark: '#E879F9'
  }
}

export function useTheme() {
  const isDark = computed(() => colorMode.value === 'dark')

  const toggleColorMode = () => {
    colorMode.value = colorMode.value === 'light' ? 'dark' : 'light'
  }

  const setColorMode = (mode) => {
    if (mode === 'light' || mode === 'dark') {
      colorMode.value = mode
    }
  }

  const setPrimaryColor = (color) => {
    if (colors[color]) {
      primaryColor.value = color
    }
  }

  const currentColor = computed(() => colors[primaryColor.value] || colors.pink)

  // Apply theme to document
  const applyTheme = () => {
    const html = document.documentElement
    
    // Apply dark mode class
    if (isDark.value) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }

    // Apply primary color (future enhancement)
    html.style.setProperty('--theme-primary', currentColor.value[colorMode.value])
  }

  // Watch for changes and apply theme
  watch([colorMode, primaryColor], applyTheme, { immediate: true })

  return {
    colorMode,
    primaryColor,
    colors,
    isDark,
    currentColor,
    toggleColorMode,
    setColorMode,
    setPrimaryColor
  }
}
