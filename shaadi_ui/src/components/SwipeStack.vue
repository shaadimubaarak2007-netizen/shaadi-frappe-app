<template>
  <div class="swipe-stack-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-card">
        <div class="animate-pulse">
          <div class="h-64 bg-gray-200 dark:bg-shaadi-dk-overlay rounded-t-2xl mb-4"></div>
          <div class="px-4 pb-4">
            <div class="h-6 bg-gray-200 dark:bg-shaadi-dk-overlay rounded w-3/4 mb-2"></div>
            <div class="h-4 bg-gray-200 dark:bg-shaadi-dk-overlay rounded w-1/2"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Swipe Stack -->
    <div v-else-if="profiles.length > 0" class="swipe-stack">
      <!-- Background Cards (for depth effect) -->
      <div
        v-for="(profile, index) in visibleProfiles"
        :key="`bg-${profile.name}`"
        v-show="index > 0 && index <= 2"
        class="background-card"
        :style="getBackgroundCardStyle(index)"
      >
        <div class="card-placeholder"></div>
      </div>

      <!-- Active Swipe Cards -->
      <SwipeCard
        v-for="(profile, index) in visibleProfiles"
        :key="profile.name"
        :profile="profile"
        :is-top-card="index === 0"
        :style="getCardStyle(index)"
        @swipe="handleSwipe"
        @drag-start="onDragStart"
        @drag-end="onDragEnd"
        ref="swipeCards"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-card">
        <FeatherIcon name="users" class="w-16 h-16 text-gray-300 mb-4" />
        <h3 class="text-xl font-semibold text-gray-600 mb-2">No more profiles</h3>
        <p class="text-gray-500 mb-6">You've seen all available matches for now</p>
        <Button variant="solid" @click="refreshProfiles">
          <template #prefix>
            <FeatherIcon name="refresh-cw" class="w-4 h-4" />
          </template>
          Refresh
        </Button>
      </div>
    </div>

    <!-- Action Buttons -->
    <div v-if="profiles.length > 0" class="action-buttons">
      <Button
        variant="outline"
        size="lg"
        class="pass-button"
        @click="swipeLeft"
        :disabled="isDragging"
      >
        <FeatherIcon name="x" class="w-6 h-6" />
      </Button>
      
      <Button
        variant="solid"
        size="lg"
        class="like-button"
        @click="swipeRight"
        :disabled="isDragging"
      >
        <FeatherIcon name="heart" class="w-6 h-6" />
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { call, Button, FeatherIcon } from 'frappe-ui'
import SwipeCard from './SwipeCard.vue'

const emit = defineEmits(['match', 'swipe', 'empty'])

// Reactive data
const profiles = ref([])
const loading = ref(true)
const isDragging = ref(false)
const swipeCards = ref([])

// Computed
const visibleProfiles = computed(() => profiles.value.slice(0, 3))

// Methods
async function loadProfiles() {
  loading.value = true
  try {
    const response = await call('shaadi.shaadi.api.matchmaking.get_swipe_queue', {
      limit: 10
    })
    // API returns {profiles: [...], total: N}, extract the profiles array
    const loadedProfiles = response?.profiles || []
    
    // Deduplicate profiles by name to avoid duplicate keys
    const uniqueProfiles = []
    const seenNames = new Set()
    
    for (const profile of loadedProfiles) {
      if (!seenNames.has(profile.name)) {
        seenNames.add(profile.name)
        uniqueProfiles.push(profile)
      }
    }
    
    profiles.value = uniqueProfiles
    
    console.log('Loaded swipe queue:', profiles.value.length, 'profiles')
    
    if (profiles.value.length === 0) {
      emit('empty')
    }
  } catch (error) {
    console.error('Error loading swipe profiles:', error)
    profiles.value = []
  } finally {
    loading.value = false
  }
}

async function handleSwipe({ action, direction, profile }) {
  try {
    // Call backend API
    const response = await call('shaadi.shaadi.api.matchmaking.swipe_profile', {
      profile_id: profile.name,
      action: action
    })
    
    // Remove swiped profile from stack
    profiles.value = profiles.value.filter(p => p.name !== profile.name)
    
    // Emit swipe event
    emit('swipe', { action, profile, response })
    
    // Check for mutual match
    if (response.mutual_match) {
      emit('match', {
        profile: response.matched_profile,
        matchData: response
      })
    }
    
    // Load more profiles if running low
    if (profiles.value.length <= 3) {
      await loadMoreProfiles()
    }
    
  } catch (error) {
    console.error('Error processing swipe:', error)
    // Reset card position on error
    await nextTick()
    if (swipeCards.value[0]) {
      // Card will snap back automatically due to error
    }
  }
}

async function loadMoreProfiles() {
  try {
    const response = await call('shaadi.shaadi.api.matchmaking.get_swipe_queue', {
      limit: 5
    })
    
    // API returns {profiles: [...], total: N}
    const newProfiles = response?.profiles || []
    
    if (newProfiles.length > 0) {
      // Add new profiles to the end
      profiles.value.push(...newProfiles)
      console.log('Loaded', newProfiles.length, 'more profiles')
    }
  } catch (error) {
    console.error('Error loading more profiles:', error)
  }
}

function swipeLeft() {
  if (swipeCards.value[0] && !isDragging.value) {
    swipeCards.value[0].swipeLeft()
  }
}

function swipeRight() {
  if (swipeCards.value[0] && !isDragging.value) {
    swipeCards.value[0].swipeRight()
  }
}

function onDragStart() {
  isDragging.value = true
}

function onDragEnd() {
  isDragging.value = false
}

function refreshProfiles() {
  loadProfiles()
}

function getCardStyle(index) {
  if (index === 0) {
    return { zIndex: 10 }
  } else if (index === 1) {
    return { 
      zIndex: 9,
      transform: 'scale(0.95) translateY(10px)',
      opacity: 0.8
    }
  } else if (index === 2) {
    return { 
      zIndex: 8,
      transform: 'scale(0.9) translateY(20px)',
      opacity: 0.6
    }
  }
  return { display: 'none' }
}

function getBackgroundCardStyle(index) {
  if (index === 1) {
    return {
      zIndex: 2,
      transform: 'scale(0.95) translateY(10px)',
      opacity: 0.3
    }
  } else if (index === 2) {
    return {
      zIndex: 1,
      transform: 'scale(0.9) translateY(20px)',
      opacity: 0.2
    }
  }
  return {}
}

// Lifecycle
onMounted(() => {
  loadProfiles()
})

// Expose methods
defineExpose({
  loadProfiles,
  refreshProfiles
})
</script>

<style scoped>
.swipe-stack-container {
  position: relative;
  width: 100%;
  height: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.swipe-stack {
  position: relative;
  width: 320px;
  height: 500px;
  margin-bottom: 40px;
}

.background-card {
  position: absolute;
  width: 320px;
  height: 500px;
  top: 0;
  left: 0;
}

.card-placeholder {
  width: 100%;
  height: 100%;
  background: #f3f4f6;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.loading-state,
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 500px;
}

.loading-card,
.empty-card {
  width: 320px;
  height: 400px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  text-align: center;
}

.action-buttons {
  display: flex;
  gap: 32px;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}

.pass-button {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 2px solid #ef4444;
  color: #ef4444;
  background: white;
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
  transition: all 0.2s ease;
}

.pass-button:hover:not(:disabled) {
  background: #ef4444;
  color: white;
  transform: scale(1.05);
}

.like-button {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ec4899, #f97316);
  color: white;
  border: none;
  box-shadow: 0 4px 16px rgba(236, 72, 153, 0.3);
  transition: all 0.2s ease;
}

.like-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4);
}

.pass-button:disabled,
.like-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .swipe-stack-container {
    height: 550px;
  }
  
  .swipe-stack {
    width: 280px;
    height: 450px;
  }
  
  .background-card {
    width: 280px;
    height: 450px;
  }
  
  .loading-card,
  .empty-card {
    width: 280px;
    height: 350px;
    padding: 24px;
  }
  
  .action-buttons {
    gap: 24px;
  }
  
  .pass-button,
  .like-button {
    width: 56px;
    height: 56px;
  }
}
</style>
