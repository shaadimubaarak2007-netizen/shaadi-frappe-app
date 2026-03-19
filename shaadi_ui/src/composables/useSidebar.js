import { ref, computed } from 'vue'
import { useStorage } from '@vueuse/core'

const sidebarCollapsed = useStorage('shaadi-sidebar-collapsed', false)
const sidebarWidth = useStorage('shaadi-sidebar-width', 256) // 16rem = 256px

export function useSidebar() {
  const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  const collapseSidebar = () => {
    sidebarCollapsed.value = true
  }

  const expandSidebar = () => {
    sidebarCollapsed.value = false
  }

  const setSidebarWidth = (width) => {
    sidebarWidth.value = width
  }

  const isCollapsed = computed(() => sidebarCollapsed.value)
  const width = computed(() => sidebarCollapsed.value ? 64 : sidebarWidth.value)

  return {
    sidebarCollapsed,
    sidebarWidth,
    isCollapsed,
    width,
    toggleSidebar,
    collapseSidebar,
    expandSidebar,
    setSidebarWidth
  }
}
