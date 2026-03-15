<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-pink-400 to-purple-500 rounded-full opacity-10 blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-purple-400 to-pink-500 rounded-full opacity-10 blur-3xl"></div>
    </div>

    <div class="flex items-center justify-center min-h-screen py-4 px-4 sm:px-6 lg:px-8">
      <div class="relative max-w-md w-full space-y-4">
        <!-- Header -->
        <div class="text-center">
          <div class="flex justify-center mb-4">
            <div class="w-12 h-12 bg-gradient-to-r from-pink-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-1">Welcome Back</h2>
          <p class="text-gray-600 dark:text-gray-300 text-sm">Sign in to find your perfect match</p>
        </div>

        <!-- Login Form -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-100 dark:border-gray-700">
          <form class="space-y-4" @submit.prevent="submit">
            <div>
              <Input
                required
                name="email"
                type="email"
                placeholder="Enter your email"
                label="Email Address"
                class="w-full"
              />
            </div>
            
            <div>
              <Input
                required
                name="password"
                type="password"
                placeholder="Enter your password"
                label="Password"
                class="w-full"
              />
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-pink-600 focus:ring-pink-500 border-gray-300 rounded">
                <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                  Remember me
                </label>
              </div>

              <div class="text-sm">
                <a href="#" class="font-medium text-pink-600 hover:text-pink-500 transition-colors">
                  Forgot your password?
                </a>
              </div>
            </div>

            <div>
              <Button 
                type="submit"
                :loading="session.login.loading" 
                class="w-full py-2 text-sm font-medium bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 text-white rounded-lg transition-all duration-200"
              >
                Sign in
              </Button>
            </div>

            <!-- Error Message -->
            <div v-if="session.login.error" class="rounded-md bg-red-50 p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">
                    {{ getErrorTitle() }}
                  </h3>
                  <div class="mt-2 text-sm text-red-700">
                    <p>{{ getErrorMessage() }}</p>
                  </div>
                </div>
              </div>
            </div>
          </form>

          <!-- Sign Up Link -->
          <div class="mt-4 text-center">
            <p class="text-sm text-gray-600">
              Don't have an account?
              <router-link to="/signup" class="font-medium text-pink-600 hover:text-pink-500 transition-colors">
                Sign up for free
              </router-link>
            </p>
          </div>
        </div>

        <!-- Footer -->
        <div class="text-center mt-2">
          <p class="text-xs text-gray-500">
            By signing in, you agree to our 
            <a href="#" class="text-pink-600 hover:text-pink-500">Terms of Service</a> and 
            <a href="#" class="text-pink-600 hover:text-pink-500">Privacy Policy</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Input, Button } from 'frappe-ui'
import { session } from "../data/session"

function submit(e) {
	const formData = new FormData(e.target)
	const credentials = {
		email: formData.get("email"),
		password: formData.get("password"),
	}
	
	// Debug logging
	console.log('Login attempt with:', {
		email: credentials.email,
		passwordLength: credentials.password && typeof credentials.password === 'string' ? credentials.password.length : 0
	})
	
	session.login.submit(credentials)
}

function getErrorTitle() {
	if (!session.login.error) return ''
	
	const error = session.login.error
	const errorMessage = error.message || error.toString()
	
	if (errorMessage.includes('AuthenticationError') || errorMessage.includes('Invalid login credentials')) {
		return 'Login Failed'
	} else if (errorMessage.includes('NetworkError') || errorMessage.includes('Connection')) {
		return 'Connection Error'
	} else {
		return 'Authentication Error'
	}
}

function getErrorMessage() {
	if (!session.login.error) return ''
	
	const error = session.login.error
	const errorMessage = error.message || error.toString()
	
	if (errorMessage.includes('AuthenticationError') || errorMessage.includes('Invalid login credentials')) {
		return 'The email or password you entered is incorrect. Please check your credentials and try again.'
	} else if (errorMessage.includes('NetworkError') || errorMessage.includes('Connection')) {
		return 'Unable to connect to the server. Please check your internet connection and try again.'
	} else if (errorMessage.includes('User does not exist') || errorMessage.includes('not found')) {
		return 'No account found with this email address. Please check your email or contact your administrator.'
	} else {
		return 'Login failed. Please try again or contact support if the problem persists.'
	}
}
</script>
