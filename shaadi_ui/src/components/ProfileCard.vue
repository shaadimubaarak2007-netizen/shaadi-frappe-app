<template>
  <Card class="profile-card hover:shadow-lg transition-shadow cursor-pointer overflow-hidden bg-shaadi-surface border-shaadi rounded-xl" @click="$emit('click', profile)">
    <div class="flex flex-col h-full min-w-0">
      <!-- Profile Photo -->
      <div class="relative mb-4">
        <img 
          v-if="profile.profile_photo && !isPhotoHidden" 
          :src="profile.profile_photo" 
          :alt="profile.full_name"
          class="w-full h-48 object-cover rounded-lg"
        />
        <div v-else class="w-full h-48 bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900 dark:to-pink-900 rounded-lg flex items-center justify-center">
          <div class="text-6xl font-bold text-purple-600 dark:text-purple-400">
            {{ getInitials(profile.full_name) }}
          </div>
        </div>
        
        <!-- Online Status Indicator -->
        <div v-if="profile.is_online" class="absolute bottom-2 left-2 bg-green-500 text-white px-2 py-1 rounded-full text-xs flex items-center gap-1">
          <div class="w-2 h-2 bg-green-300 rounded-full animate-pulse"></div>
          Online
        </div>
        
        <!-- Match Percentage Badge -->
        <div v-if="profile.match_score" class="absolute top-2 right-2">
          <MatchPercentage :score="profile.match_score" size="sm" />
        </div>
        
        <!-- Verified Badge -->
        <div v-if="profile.verified" class="absolute top-2 left-2 bg-blue-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 shadow-md">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          Verified
        </div>
        
        <!-- Interest Sent Badge -->
        <div v-if="interestSent" class="absolute top-2 left-2 bg-gradient-to-r from-pink-500 to-pink-600 text-white px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1 shadow-lg">
          <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/>
          </svg>
          Liked
        </div>
      </div>

      <!-- Profile Info -->
      <div class="flex-1 min-w-0">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1 truncate" :title="profile.full_name">{{ profile.full_name }}</h3>
        <div class="text-sm text-gray-600 dark:text-gray-300 space-y-1">
          <div class="flex items-center gap-2">
            <span>{{ profile.age }} years</span>
            <span v-if="profile.height_cm">• {{ formatHeight(profile.height_cm) }}</span>
          </div>
          <div v-if="profile.education" class="truncate text-gray-600 dark:text-gray-300" :title="profile.education">{{ profile.education }}</div>
          <div v-if="profile.occupation" class="truncate text-gray-600 dark:text-gray-300" :title="profile.occupation">{{ profile.occupation }}</div>
          <div v-if="profile.city" class="flex items-center gap-1 min-w-0 text-gray-600 dark:text-gray-300">
            <svg class="w-4 h-4 flex-shrink-0 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            <span class="truncate" :title="`${profile.city}${profile.state ? ', ' + profile.state : ''}`">
              {{ profile.city }}<span v-if="profile.state">, {{ profile.state }}</span>
            </span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-2">
        <Button 
          v-if="showActions"
          :variant="interestSent ? 'outline' : 'solid'"
          size="sm"
          class="flex-1"
          :disabled="interestSent"
          @click.stop="$emit('sendInterest', profile)"
        >
          <template #prefix>
            <FeatherIcon :name="interestSent ? 'check' : 'heart'" class="w-4 h-4" />
          </template>
          {{ interestSent ? 'Interest Sent' : 'Send Interest' }}
        </Button>
        <Button 
          v-if="showActions"
          variant="outline"
          size="sm"
          @click.stop="$emit('shortlist', profile)"
        >
          <FeatherIcon name="star" class="w-4 h-4" />
        </Button>
      </div>
    </div>
  </Card>
</template>

<script setup>
import { computed } from 'vue'
import { Button, Card, FeatherIcon } from 'frappe-ui'
import MatchPercentage from './MatchPercentage.vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  },
  interestSent: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click', 'send-interest', 'shortlist'])

const isPhotoHidden = computed(() => {
  // Check if photo should be hidden based on privacy settings
  return props.profile.photo_hidden || false
})

function getInitials(name) {
  if (!name) return '?'
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

function formatHeight(cm) {
  const feet = Math.floor(cm / 30.48)
  const inches = Math.round((cm % 30.48) / 2.54)
  return `${feet}'${inches}"`
}
</script>

<style scoped>
.profile-card {
  @apply transition-all duration-200;
}

.profile-card:hover {
  @apply transform -translate-y-1;
}
</style>
