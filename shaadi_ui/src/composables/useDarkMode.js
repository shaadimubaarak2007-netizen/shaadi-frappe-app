import { ref, onMounted } from 'vue'

const isDark = ref(true)

export function useDarkMode() {
  function setTheme(dark) {
    isDark.value = dark
    // Set both class and data-theme for Frappe UI compatibility
    document.documentElement.classList.toggle('dark', dark)
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
    localStorage.setItem('shaadi-theme', dark ? 'dark' : 'light')
  }

  function toggleTheme() {
    setTheme(!isDark.value)
  }

  onMounted(() => {
    // Check localStorage first
    const savedTheme = localStorage.getItem('shaadi-theme')
    if (savedTheme) {
      setTheme(savedTheme === 'dark')
    } else {
      // Default to dark mode
      setTheme(true)
    }

    // Watch for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = (e) => {
      if (!localStorage.getItem('shaadi-theme')) {
        setTheme(e.matches)
      }
    }
    mediaQuery.addEventListener('change', handleChange)
  })

  return {
    isDark,
    toggleTheme,
    setTheme
  }
}
