<template>
  <div v-if="pwa.isInstallable && !pwa.isInstalled && !dismissed" 
       class="fixed bottom-0 left-0 right-0 z-50 md:bottom-4 md:left-4 md:right-auto md:max-w-md animate-slide-up">
    <div class="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-4 rounded-t-lg md:rounded-lg shadow-2xl">
      <div class="flex items-start justify-between">
        <div class="flex items-start flex-1">
          <div class="w-12 h-12 bg-white rounded-lg flex items-center justify-center mr-3 flex-shrink-0">
            <FeatherIcon name="heart" class="w-6 h-6 text-pink-600" />
          </div>
          <div class="flex-1">
            <h3 class="font-bold text-lg mb-1">Install Shaadi App</h3>
            <p class="text-sm text-pink-100 mb-3">
              Get the full app experience with offline access and instant notifications
            </p>
            <div class="flex space-x-2">
              <Button 
                @click="handleInstall" 
                variant="solid"
                class="bg-white text-pink-600 hover:bg-pink-50"
                size="sm"
              >
                <template #prefix>
                  <FeatherIcon name="download" class="w-4 h-4" />
                </template>
                Install Now
              </Button>
              <Button 
                @click="dismiss" 
                variant="ghost"
                class="text-white hover:bg-white/20"
                size="sm"
              >
                Maybe Later
              </Button>
            </div>
          </div>
        </div>
        <button @click="dismiss" class="text-white/80 hover:text-white ml-2">
          <FeatherIcon name="x" class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePWA } from '@/composables/usePWA'
import { Button, FeatherIcon } from 'frappe-ui'

const pwa = usePWA()
const dismissed = ref(false)

const handleInstall = () => {
  pwa.install()
  dismissed.value = true
}

const dismiss = () => {
  dismissed.value = true
  // Store dismissal in localStorage to not show again for 7 days
  localStorage.setItem('pwa-install-dismissed', Date.now().toString())
}

// Check if banner was recently dismissed
const checkDismissed = () => {
  const dismissedTime = localStorage.getItem('pwa-install-dismissed')
  if (dismissedTime) {
    const sevenDays = 7 * 24 * 60 * 60 * 1000
    if (Date.now() - parseInt(dismissedTime) < sevenDays) {
      dismissed.value = true
    }
  }
}

checkDismissed()
</script>

<style scoped>
@keyframes slide-up {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}
</style>
