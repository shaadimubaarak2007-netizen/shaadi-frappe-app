import { io } from "socket.io-client"

let socket = null
let isInitialized = false

export function initSocket() {
	if (isInitialized && socket) {
		return socket
	}

	try {
		// Get site name from window or default
		const siteName = window.site_name || 'shaadi.amitkumar.live'
		const host = window.location.hostname
		const port = window.location.port
		
		// Frappe's socketio server runs on port 9000 by default
		const socketPort = port === '8080' ? '9000' : (port || '9000')
		const protocol = window.location.protocol === 'https:' ? 'https' : 'http'
		
		// Connect to Frappe's realtime server with site namespace
		const url = `${protocol}://${host}:${socketPort}/${siteName}`
		
		console.log('Initializing socket connection to:', url)
		
		socket = io(url, {
			withCredentials: true,
			reconnectionAttempts: 5,
			reconnectionDelay: 1000,
			transports: ['websocket', 'polling'],
			auth: {
				// Frappe uses cookies for authentication
				// Socket.io will automatically send cookies
			}
		})

		socket.on('connect', () => {
			console.log('Socket connected successfully')
			isInitialized = true
		})

		socket.on('connect_error', (error) => {
			console.warn('Socket connection error:', error.message)
		})

		socket.on('disconnect', (reason) => {
			console.log('Socket disconnected:', reason)
			if (reason === 'io server disconnect') {
				// Server disconnected, try to reconnect
				socket.connect()
			}
		})

		// Listen for real-time events
		socket.on('interest_sent', (data) => {
			console.log('Interest sent event:', data)
			// Handle interest sent notification
		})

		socket.on('profile_shortlisted', (data) => {
			console.log('Profile shortlisted event:', data)
			// Handle shortlist notification
		})

		socket.on('interest_response', (data) => {
			console.log('Interest response event:', data)
			// Handle interest response (accepted/declined)
		})

		// Swipe matching events
		socket.on('mutual_match', (data) => {
			console.log('Mutual match event:', data)
			
			// Show browser notification if permission granted
			if (Notification.permission === 'granted') {
				new Notification('🎉 It\'s a Match!', {
					body: `You and ${data.user2} liked each other!`,
					icon: '/assets/heart-icon.png',
					tag: 'mutual-match'
				})
			}
			
			// Emit custom event for components to listen to
			window.dispatchEvent(new CustomEvent('mutualMatch', {
				detail: data
			}))
		})

		socket.on('profile_liked', (data) => {
			console.log('Profile liked event:', data)
			
			// Show subtle notification for likes received
			if (Notification.permission === 'granted') {
				new Notification('Someone liked your profile!', {
					body: 'Check your matches to see who it is',
					icon: '/assets/heart-icon.png',
					tag: 'profile-liked'
				})
			}
			
			// Emit custom event
			window.dispatchEvent(new CustomEvent('profileLiked', {
				detail: data
			}))
		})

		return socket
	} catch (error) {
		console.error('Failed to initialize socket:', error)
		return null
	}
}

export function useSocket() {
	return socket
}

export function getSocket() {
	if (!socket || !isInitialized) {
		return initSocket()
	}
	return socket
}
