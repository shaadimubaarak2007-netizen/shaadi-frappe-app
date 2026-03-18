import { ref, onMounted } from 'vue'

export function usePWA() {
  const isInstallable = ref(false)
  const isInstalled = ref(false)
  const deferredPrompt = ref(null)

  const install = async () => {
    if (!deferredPrompt.value) {
      console.log('No deferred prompt available')
      return
    }
    
    // Show the install prompt
    deferredPrompt.value.prompt()
    
    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.value.userChoice
    
    if (outcome === 'accepted') {
      console.log('PWA installation accepted')
      isInstallable.value = false
    } else {
      console.log('PWA installation dismissed')
    }
    
    // Clear the deferred prompt
    deferredPrompt.value = null
  }

  const checkInstalled = () => {
    // Check if app is running in standalone mode
    if (window.matchMedia('(display-mode: standalone)').matches) {
      isInstalled.value = true
      console.log('App is running in standalone mode')
    }
    
    // Also check for iOS standalone mode
    if (window.navigator.standalone === true) {
      isInstalled.value = true
      console.log('App is running in iOS standalone mode')
    }
  }

  onMounted(() => {
    // Listen for beforeinstallprompt event
    window.addEventListener('beforeinstallprompt', (e) => {
      console.log('beforeinstallprompt event fired')
      e.preventDefault()
      deferredPrompt.value = e
      isInstallable.value = true
    })

    // Listen for app installed event
    window.addEventListener('appinstalled', () => {
      console.log('PWA was installed')
      isInstalled.value = true
      isInstallable.value = false
    })

    // Check if already installed
    checkInstalled()
  })

  return {
    isInstallable,
    isInstalled,
    install
  }
}
