<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden">
    <!-- Sidebar -->
    <aside
      :class="[
        'flex flex-col bg-white border-r border-gray-200 transition-all duration-300 ease-in-out',
        isCollapsed ? 'w-16' : 'w-64'
      ]"
    >
      <!-- Header: Logo/Brand -->
      <div class="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        <router-link to="/dashboard" class="flex items-center space-x-2">
          <div class="w-10 h-10 bg-gradient-to-br from-pink-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0">
            <FeatherIcon name="heart" class="w-6 h-6 text-white" />
          </div>
          <span
            v-if="!isCollapsed"
            class="text-xl font-bold text-gradient-primary transition-opacity duration-200"
          >
            Shaadi
          </span>
        </router-link>
        
        <Button
          icon="chevrons-left"
          variant="ghost"
          size="sm"
          class="flex-shrink-0"
          :class="{ 'rotate-180': isCollapsed }"
          @click="toggleSidebar"
        />
      </div>

      <!-- Search Button -->
      <div class="p-2">
        <Button
          :icon="isCollapsed ? 'search' : undefined"
          :label="isCollapsed ? undefined : 'Search...'"
          variant="ghost"
          block
          class="justify-start text-gray-600 hover:text-gray-900 hover:bg-gray-100"
          @click="$emit('open-search')"
        >
          <template v-if="!isCollapsed" #prefix>
            <FeatherIcon name="search" class="w-4 h-4" />
          </template>
          <template v-if="!isCollapsed" #suffix>
            <kbd class="px-1.5 py-0.5 text-xs bg-gray-100 border border-gray-200 rounded">
              ⌘K
            </kbd>
          </template>
        </Button>
      </div>

      <!-- Navigation Links -->
      <nav class="flex-1 px-2 py-2 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          v-slot="{ isActive }"
          custom
        >
          <Button
            :icon="item.icon"
            :label="isCollapsed ? undefined : item.label"
            variant="ghost"
            block
            class="justify-start"
            :class="[
              isActive
                ? 'bg-pink-50 text-pink-600 hover:bg-pink-100'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            ]"
            @click="$router.push(item.path)"
          >
            <template v-if="!isCollapsed && item.badge" #suffix>
              <Badge variant="subtle" size="sm" class="bg-pink-100 text-pink-600">
                {{ item.badge }}
              </Badge>
            </template>
          </Button>
        </router-link>
      </nav>

      <!-- Footer: User Menu -->
      <div class="p-2 border-t border-gray-200">
        <Dropdown :options="userMenuOptions" :placement="isCollapsed ? 'right' : 'top'">
          <Button
            :avatar="userPhoto"
            :label="isCollapsed ? undefined : userName"
            variant="ghost"
            block
            class="justify-start"
          >
            <template v-if="!isCollapsed" #suffix>
              <FeatherIcon name="chevrons-up-down" class="w-4 h-4 text-gray-400" />
            </template>
          </Button>
        </Dropdown>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Navbar (if slot provided) -->
      <header v-if="$slots.navbar" class="bg-white border-b border-gray-200">
        <slot name="navbar" />
      </header>

      <!-- Toolbar (if slot provided) -->
      <div v-if="$slots.toolbar" class="bg-white border-b border-gray-200">
        <slot name="toolbar" />
      </div>

      <!-- Page Content -->
      <div class="flex-1 overflow-y-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <slot />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Badge, Dropdown, FeatherIcon } from 'frappe-ui'
import { useSidebar } from '@/composables/useSidebar'
import { session } from '@/data/session'

const router = useRouter()
const { isCollapsed, toggleSidebar } = useSidebar()

defineEmits(['open-search'])

const navItems = [
  {
    label: 'Dashboard',
    path: '/dashboard',
    icon: 'home',
    badge: null
  },
  {
    label: 'Browse',
    path: '/browse',
    icon: 'search',
    badge: null
  },
  {
    label: 'Matches',
    path: '/matches',
    icon: 'users',
    badge: '12'
  },
  {
    label: 'Interests',
    path: '/interests',
    icon: 'heart',
    badge: '5'
  },
  {
    label: 'Messages',
    path: '/messages',
    icon: 'message-circle',
    badge: '3'
  },
  {
    label: 'Shortlist',
    path: '/shortlist',
    icon: 'star',
    badge: null
  }
]

const userName = computed(() => session.user?.full_name || session.user?.email || 'User')
const userPhoto = computed(() => session.user?.user_image)

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
    onClick: () => {
      // Install app logic (already implemented in Navigation.vue)
      console.log('Install app clicked')
    }
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
</script>

<style scoped>
.text-gradient-primary {
  background: linear-gradient(135deg, #EC4899 0%, #9333EA 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.rotate-180 {
  transform: rotate(180deg);
}

/* Smooth transitions */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Custom scrollbar */
nav::-webkit-scrollbar {
  width: 6px;
}

nav::-webkit-scrollbar-track {
  background: transparent;
}

nav::-webkit-scrollbar-thumb {
  background: #E5E7EB;
  border-radius: 3px;
}

nav::-webkit-scrollbar-thumb:hover {
  background: #D1D5DB;
}
</style>
