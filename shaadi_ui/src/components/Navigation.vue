<template>
  <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-10 h-10 bg-gradient-to-br from-pink-500 to-purple-600 rounded-lg flex items-center justify-center">
              <FeatherIcon name="heart" class="w-6 h-6 text-white" />
            </div>
            <span class="text-xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
              Shaadi
            </span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div v-if="isLoggedIn" class="hidden md:flex items-center space-x-1">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
            :class="isActive(item.path) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
          >
            <div class="flex items-center space-x-2">
              <FeatherIcon :name="item.icon" class="w-4 h-4" />
              <span>{{ item.label }}</span>
            </div>
          </router-link>
        </div>

        <!-- Right Side - Auth Buttons or User Menu -->
        <div class="flex items-center space-x-4">
          <template v-if="!isLoggedIn">
            <Button variant="subtle" size="md" @click="$router.push('/signin')">
              Login
            </Button>
            <Button variant="solid" size="md" @click="$router.push('/signup')">
              Sign Up
            </Button>
          </template>
          <template v-else>
            <!-- Notifications -->
            <div class="relative z-[60]">
              <Dropdown :options="notificationOptions">
                <template #default="{ open }">
                  <Button variant="ghost" size="md" class="relative">
                    <FeatherIcon name="bell" class="w-5 h-5" />
                    <span v-if="unreadCount > 0" class="absolute top-0 right-0 px-1.5 py-0.5 text-xs bg-red-500 text-white rounded-full min-w-[1.25rem] flex items-center justify-center">
                      {{ unreadCount > 9 ? '9+' : unreadCount }}
                    </span>
                  </Button>
                </template>
              </Dropdown>
            </div>

            <!-- User Menu -->
            <div class="relative z-[60]">
              <Dropdown :options="userMenuOptions">
                <template #default="{ open }">
                  <button class="flex items-center space-x-2 px-3 py-2 rounded-md hover:bg-gray-50 transition-colors">
                    <Avatar 
                      :label="userInitials" 
                      :image="userPhoto"
                      size="sm"
                      class="bg-gradient-to-br from-pink-500 to-purple-600"
                    />
                    <span class="text-sm font-medium text-gray-700 hidden md:block">
                      {{ userName }}
                    </span>
                    <FeatherIcon name="chevron-down" class="w-4 h-4 text-gray-400" />
                  </button>
                </template>
              </Dropdown>
            </div>
          </template>

          <!-- Mobile Menu Button -->
          <Button 
            v-if="isLoggedIn"
            variant="ghost" 
            size="md" 
            class="md:hidden"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <FeatherIcon :name="mobileMenuOpen ? 'x' : 'menu'" class="w-5 h-5" />
          </Button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="isLoggedIn && mobileMenuOpen" class="md:hidden border-t border-gray-200">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          @click="mobileMenuOpen = false"
          class="flex items-center space-x-3 px-3 py-2 rounded-md text-base font-medium transition-colors"
          :class="isActive(item.path) ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
        >
          <FeatherIcon :name="item.icon" class="w-5 h-5" />
          <span>{{ item.label }}</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Button, Avatar, Dropdown, FeatherIcon, call } from 'frappe-ui'
import { session } from '@/data/session'
import { useNotifications } from '@/composables/useNotifications'
import { usePWA } from '@/composables/usePWA'

const router = useRouter()
const route = useRoute()
const mobileMenuOpen = ref(false)
const notifications = ref([])
const pwa = usePWA()

// Use shared notification state for real-time updates
const { unreadCount, loadUnreadCount, setupRealtimeUpdates, cleanupRealtimeUpdates } = useNotifications()

const userProfile = ref({
  full_name: 'User',
  profile_photo: null,
  email: ''
})

const isLoggedIn = computed(() => session.isLoggedIn)
const userName = computed(() => userProfile.value.full_name || session.user?.full_name || session.user?.email || 'User')
const userPhoto = computed(() => userProfile.value.profile_photo)
const userInitials = computed(() => {
  const name = userName.value
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const notificationOptions = computed(() => {
  const options = notifications.value.slice(0, 5).map(notif => ({
    label: notif.sender_name || 'Unknown',
    description: notif.message || 'New message',
    icon: getNotificationIcon(notif.type),
    avatar: notif.sender_photo,
    badge: notif.unread_count > 1 ? notif.unread_count.toString() : null,
    timestamp: formatNotificationTime(notif.timestamp),
    onClick: () => handleNotificationClick(notif)
  }))
  
  if (notifications.value.length > 5) {
    options.push({
      label: 'View all notifications',
      icon: 'arrow-right',
      onClick: () => router.push('/messages')
    })
  }
  
  if (options.length === 0) {
    options.push({
      label: 'No new notifications',
      icon: 'bell',
      disabled: true
    })
  }
  
  return options
})

const menuItems = [
  { label: 'Dashboard', path: '/dashboard', icon: 'home' },
  { label: 'Browse', path: '/browse', icon: 'search' },
  { label: 'Matches', path: '/matches', icon: 'users' },
  { label: 'Interests', path: '/interests', icon: 'heart' },
  { label: 'Messages', path: '/messages', icon: 'message-circle' },
  { label: 'Shortlist', path: '/shortlist', icon: 'star' }
]

const handleInstallApp = () => {
  if (pwa.isInstalled.value) {
    alert('App is already installed on your device!')
  } else if (pwa.isInstallable.value) {
    pwa.install()
  } else {
    // Show instructions for manual installation (especially for iOS)
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent)
    if (isIOS) {
      alert('To install on iOS:\n1. Tap the Share button\n2. Scroll down and tap "Add to Home Screen"\n3. Tap "Add" to confirm')
    } else {
      alert('Installation is not available on this browser. Please use Chrome, Edge, or Safari for the best experience.')
    }
  }
}

const userMenuOptions = [
  {
    label: 'My Profile',
    icon: 'user',
    onClick: () => router.push('/my-profile')
  },
  {
    label: 'Partner Preferences',
    icon: 'sliders',
    onClick: () => router.push('/preferences')
  },
  {
    label: 'Settings',
    icon: 'settings',
    onClick: () => router.push('/settings')
  },
  {
    label: 'Subscription',
    icon: 'zap',
    onClick: () => router.push('/subscription')
  },
  {
    label: 'Install App',
    icon: 'download',
    onClick: handleInstallApp
  },
  {
    label: 'Logout',
    icon: 'log-out',
    onClick: () => {
      session.logout.submit()
      router.push('/signin')
    }
  }
]

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/')
}

async function loadNotifications() {
  if (!isLoggedIn.value) return
  
  try {
    // Load detailed notifications with sender info
    const response = await call('shaadi.shaadi.api.messaging.get_notifications')
    notifications.value = response?.notifications || []
    unreadCount.value = response?.unread_count || 0
  } catch (error) {
    console.error('Error loading notifications:', error)
    // Fallback to basic unread count
    await loadUnreadCount()
    notifications.value = []
  }
}

async function loadUserProfile() {
  if (!isLoggedIn.value) return
  
  try {
    const response = await call('shaadi.shaadi.api.messaging.get_current_user_profile')
    if (response) {
      userProfile.value = {
        full_name: response.full_name || 'User',
        profile_photo: response.profile_photo,
        email: response.email || ''
      }
    }
  } catch (error) {
    console.error('Error loading user profile:', error)
  }
}

function getNotificationIcon(type) {
  const iconMap = {
    'interest': 'heart',
    'message': 'message-circle',
    'profile_view': 'eye',
    'match': 'users',
    'subscription': 'zap'
  }
  return iconMap[type] || 'bell'
}

function formatNotificationTime(timestamp) {
  if (!timestamp) return ''
  
  const now = new Date()
  const time = new Date(timestamp)
  const diffMs = now - time
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`
  if (diffDays < 7) return `${diffDays}d ago`
  
  return time.toLocaleDateString()
}

async function handleNotificationClick(notification) {
  try {
    // Navigate to the conversation
    if (notification.link) {
      router.push(notification.link)
    }
    
    // Reload notifications after navigation
    setTimeout(() => {
      loadNotifications()
    }, 1000)
  } catch (error) {
    console.error('Error handling notification:', error)
  }
}

// Load notifications when component mounts and user is logged in
onMounted(async () => {
  if (isLoggedIn.value) {
    await loadUserProfile()
    await loadNotifications()
    setupRealtimeUpdates()
  }
})

onUnmounted(() => {
  cleanupRealtimeUpdates()
})

watch(isLoggedIn, async (newVal) => {
  if (newVal) {
    await loadUserProfile()
    await loadNotifications()
    setupRealtimeUpdates()
  } else {
    cleanupRealtimeUpdates()
    userProfile.value = { full_name: 'User', profile_photo: null, email: '' }
  }
})
</script>
