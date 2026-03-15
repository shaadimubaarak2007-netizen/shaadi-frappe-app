<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
    <!-- Hero Section -->
    <section class="relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <!-- Left Content -->
          <div class="text-center lg:text-left">
            <h1 class="text-4xl lg:text-6xl font-bold text-gray-900 mb-6">
              Find Your
              <span class="bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
                Perfect Match
              </span>
            </h1>
            <p class="text-xl text-gray-600 mb-8">
              India's most trusted matrimonial platform. Join millions of happy couples who found their life partner with us.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button variant="solid" size="lg" @click="$router.push('/signup')" class="text-lg px-8 py-3">
                <template #prefix>
                  <FeatherIcon name="heart" class="w-5 h-5" />
                </template>
                Get Started Free
              </Button>
              <Button variant="outline" size="lg" @click="$router.push('/browse')" class="text-lg px-8 py-3">
                <template #prefix>
                  <FeatherIcon name="search" class="w-5 h-5" />
                </template>
                Browse Profiles
              </Button>
            </div>
            
            <!-- Stats -->
            <div class="grid grid-cols-3 gap-6 mt-12">
              <div class="text-center">
                <div class="text-3xl font-bold text-pink-600">10M+</div>
                <div class="text-sm text-gray-600">Happy Couples</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-purple-600">50M+</div>
                <div class="text-sm text-gray-600">Profiles</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-blue-600">100%</div>
                <div class="text-sm text-gray-600">Verified</div>
              </div>
            </div>
          </div>

          <!-- Right Image/Illustration -->
          <div class="relative">
            <div class="relative z-10 bg-white rounded-2xl shadow-2xl p-8">
              <div class="aspect-square bg-gradient-to-br from-pink-100 to-purple-100 rounded-xl flex items-center justify-center">
                <FeatherIcon name="heart" class="w-32 h-32 text-pink-500" />
              </div>
            </div>
            <!-- Decorative elements -->
            <div class="absolute -top-4 -right-4 w-72 h-72 bg-pink-200 rounded-full opacity-20 blur-3xl"></div>
            <div class="absolute -bottom-4 -left-4 w-72 h-72 bg-purple-200 rounded-full opacity-20 blur-3xl"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Why Choose Shaadi?
          </h2>
          <p class="text-xl text-gray-600">
            Your journey to finding the perfect life partner starts here
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <Card v-for="feature in features" :key="feature.title" class="text-center p-6 hover:shadow-lg transition-shadow">
            <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full mb-4">
              <FeatherIcon :name="feature.icon" class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ feature.title }}</h3>
            <p class="text-gray-600">{{ feature.description }}</p>
          </Card>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            How It Works
          </h2>
          <p class="text-xl text-gray-600">
            Simple steps to find your perfect match
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="(step, index) in steps" :key="step.title" class="relative">
            <div class="text-center">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full text-white text-2xl font-bold mb-4">
                {{ index + 1 }}
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ step.title }}</h3>
              <p class="text-gray-600">{{ step.description }}</p>
            </div>
            <div v-if="index < steps.length - 1" class="hidden md:block absolute top-8 left-1/2 w-full h-0.5 bg-gradient-to-r from-pink-300 to-purple-300"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-pink-600 to-purple-600">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl lg:text-4xl font-bold text-white mb-4">
          Ready to Find Your Life Partner?
        </h2>
        <p class="text-xl text-pink-100 mb-8">
          Join millions of happy couples. Start your journey today!
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <Button variant="solid" size="lg" @click="$router.push('/signup')" class="bg-white text-pink-600 hover:bg-gray-50 text-lg px-8 py-3">
            <template #prefix>
              <FeatherIcon name="user-plus" class="w-5 h-5" />
            </template>
            Create Free Account
          </Button>
          <Button variant="outline" size="lg" @click="$router.push('/signin')" class="border-white text-white hover:bg-white/10 text-lg px-8 py-3">
            <template #prefix>
              <FeatherIcon name="log-in" class="w-5 h-5" />
            </template>
            Login
          </Button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-8 h-8 bg-gradient-to-br from-pink-500 to-purple-600 rounded-lg flex items-center justify-center">
                <FeatherIcon name="heart" class="w-5 h-5 text-white" />
              </div>
              <span class="text-xl font-bold text-white">Shaadi</span>
            </div>
            <p class="text-sm">India's most trusted matrimonial platform</p>
          </div>
          <div>
            <h4 class="font-semibold text-white mb-4">Company</h4>
            <ul class="space-y-2 text-sm">
              <li><a href="#" class="hover:text-white">About Us</a></li>
              <li><a href="#" class="hover:text-white">Contact</a></li>
              <li><a href="#" class="hover:text-white">Careers</a></li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold text-white mb-4">Support</h4>
            <ul class="space-y-2 text-sm">
              <li><a href="#" class="hover:text-white">Help Center</a></li>
              <li><a href="#" class="hover:text-white">Safety Tips</a></li>
              <li><a href="#" class="hover:text-white">Terms of Service</a></li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold text-white mb-4">Connect</h4>
            <div class="flex space-x-4">
              <a href="#" class="hover:text-white"><FeatherIcon name="facebook" class="w-5 h-5" /></a>
              <a href="#" class="hover:text-white"><FeatherIcon name="twitter" class="w-5 h-5" /></a>
              <a href="#" class="hover:text-white"><FeatherIcon name="instagram" class="w-5 h-5" /></a>
            </div>
          </div>
        </div>
        <div class="border-t border-gray-800 pt-8 text-center text-sm">
          <p>&copy; 2026 Shaadi. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, Card, FeatherIcon } from 'frappe-ui'

const features = [
  {
    icon: 'shield',
    title: '100% Verified',
    description: 'All profiles are manually verified for authenticity and safety'
  },
  {
    icon: 'users',
    title: 'Smart Matching',
    description: 'Advanced algorithm to find your most compatible matches'
  },
  {
    icon: 'lock',
    title: 'Privacy First',
    description: 'Your data is secure with industry-leading encryption'
  },
  {
    icon: 'zap',
    title: 'Quick Connect',
    description: 'Express interest and connect with matches instantly'
  }
]

const steps = [
  {
    title: 'Create Profile',
    description: 'Sign up and create your detailed profile in minutes'
  },
  {
    title: 'Find Matches',
    description: 'Browse through verified profiles that match your preferences'
  },
  {
    title: 'Connect & Chat',
    description: 'Send interests and start meaningful conversations'
  }
]
</script>
