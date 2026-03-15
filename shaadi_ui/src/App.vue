<template>
  <div>
    <Navigation />
    <router-view />
    
    <!-- Footer with Developer Credits -->
    <footer class="bg-white border-t border-gray-200 py-4 mt-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <p class="text-sm text-gray-600">
            Made with love ❤️ by 
            <a 
              href="https://resume.amitkumar.live/" 
              target="_blank" 
              rel="noopener noreferrer"
              class="text-pink-600 hover:text-pink-700 font-medium transition-colors duration-200"
            >
              Amit Kumar
            </a>
          </p>
        </div>
      </div>
    </footer>
    
    <!-- Preference Setup Modal -->
    <PreferenceSetupModal
      v-model="showPreferenceModal"
      @saved="onPreferencesSaved"
      @skipped="onPreferencesSkipped"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navigation from '@/components/Navigation.vue'
import PreferenceSetupModal from '@/components/PreferenceSetupModal.vue'
import { call } from 'frappe-ui'
import { session } from './data/session'

const router = useRouter()
const route = useRoute()
const showPreferenceModal = ref(false)
const preferenceCheckDone = ref(false)

async function checkPartnerPreferences() {
  // Only check if user is logged in and not on auth pages
  if (!session.isLoggedIn) return
  if (route.path === '/signin' || route.path === '/signup' || route.path === '/') return
  if (preferenceCheckDone.value) return
  
  try {
    const response = await call('shaadi.shaadi.api.partner_preference.check_preference_exists')
    
    if (!response.exists) {
      // Check if user has dismissed the modal in this session
      const dismissed = sessionStorage.getItem('preference_modal_dismissed')
      if (!dismissed) {
        // Show modal after a short delay to let the page load
        setTimeout(() => {
          showPreferenceModal.value = true
        }, 1500)
      }
    }
    
    preferenceCheckDone.value = true
  } catch (error) {
    console.error('Error checking preferences:', error)
  }
}

function onPreferencesSaved() {
  showPreferenceModal.value = false
  sessionStorage.removeItem('preference_modal_dismissed')
}

function onPreferencesSkipped() {
  showPreferenceModal.value = false
  // Remember that user skipped in this session
  sessionStorage.setItem('preference_modal_dismissed', 'true')
}

// Check preferences when app mounts and when route changes
onMounted(() => {
  checkPartnerPreferences()
})

// Watch for route changes to check preferences
router.afterEach(() => {
  if (!preferenceCheckDone.value) {
    checkPartnerPreferences()
  }
})
</script>
