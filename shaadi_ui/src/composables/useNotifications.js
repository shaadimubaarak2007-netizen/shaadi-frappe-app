import { ref, onMounted, onUnmounted } from 'vue'
import { call } from 'frappe-ui'
import { getSocket } from '@/socket'

const unreadCount = ref(0)
const socket = getSocket()

export function useNotifications() {
  async function loadUnreadCount() {
    try {
      const response = await call('shaadi.shaadi.api.messaging.get_unread_count')
      unreadCount.value = response?.unread_count || 0
    } catch (error) {
      console.error('Error loading unread count:', error)
    }
  }

  function handleNewMessage(data) {
    // Increment unread count when new message arrives
    if (!data.is_own_message) {
      unreadCount.value++
    }
  }

  function decrementUnreadCount(count = 1) {
    unreadCount.value = Math.max(0, unreadCount.value - count)
  }

  function setupRealtimeUpdates() {
    if (socket) {
      socket.on('new_message', handleNewMessage)
    }
  }

  function cleanupRealtimeUpdates() {
    if (socket) {
      socket.off('new_message', handleNewMessage)
    }
  }

  return {
    unreadCount,
    loadUnreadCount,
    decrementUnreadCount,
    setupRealtimeUpdates,
    cleanupRealtimeUpdates
  }
}
