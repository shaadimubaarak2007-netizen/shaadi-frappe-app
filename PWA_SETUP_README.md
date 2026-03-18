# PWA Setup Guide for Shaadi App

## ✅ Implementation Complete

All PWA components have been implemented following best practices from Google's web.dev and vue-pwa-install patterns.

---

## 📁 Files Created

### 1. **Manifest** (`/shaadi_ui/public/manifest.json`)
- App name, description, theme colors
- Icons configuration (8 sizes)
- Shortcuts for quick access
- Display mode: standalone

### 2. **Service Worker** (`/shaadi_ui/public/sw.js`)
- Offline caching strategy
- Cache-first fetch approach
- Automatic cache cleanup
- Offline fallback

### 3. **PWA Composable** (`/shaadi_ui/src/composables/usePWA.js`)
- Captures `beforeinstallprompt` event
- Provides install() method
- Detects if app is already installed
- Tracks installation state

### 4. **Install Banner** (`/shaadi_ui/src/components/InstallBanner.vue`)
- Beautiful gradient banner
- Auto-dismissal with 7-day cooldown
- Slide-up animation
- Mobile-responsive

### 5. **Icon Source** (`/shaadi_ui/public/icons/icon-source.svg`)
- Purple-to-pink gradient
- White heart icon
- 512x512 scalable SVG

### 6. **Updated index.html**
- PWA meta tags (iOS + Android)
- Manifest link
- Apple touch icons
- Service worker registration

---

## 🎨 Icon Generation Required

You need to generate PNG icons from the SVG source. Use one of these tools:

### Option 1: Online Tools
- **PWA Builder**: https://www.pwabuilder.com/imageGenerator
- **RealFaviconGenerator**: https://realfavicongenerator.net/
- **Maskable.app**: https://maskable.app/ (for maskable icons)

### Option 2: Command Line (ImageMagick)

```bash
cd /home/erpnext/frappe-bench/apps/shaadi/shaadi_ui/public/icons

# Convert SVG to PNG at different sizes
convert icon-source.svg -resize 16x16 icon-16x16.png
convert icon-source.svg -resize 32x32 icon-32x32.png
convert icon-source.svg -resize 72x72 icon-72x72.png
convert icon-source.svg -resize 96x96 icon-96x96.png
convert icon-source.svg -resize 128x128 icon-128x128.png
convert icon-source.svg -resize 144x144 icon-144x144.png
convert icon-source.svg -resize 152x152 icon-152x152.png
convert icon-source.svg -resize 180x180 icon-180x180.png
convert icon-source.svg -resize 192x192 icon-192x192.png
convert icon-source.svg -resize 384x384 icon-384x384.png
convert icon-source.svg -resize 512x512 icon-512x512.png
```

### Required Icon Sizes:
- ✅ 16x16, 32x32 (Favicon)
- ✅ 72x72, 96x96, 128x128, 144x144, 152x152 (iOS)
- ✅ 180x180 (Apple Touch Icon)
- ✅ 192x192, 384x384, 512x512 (Android)

---

## 🚀 How It Works

### 1. **Install Prompt Flow**

```
User visits Shaadi → Browser checks PWA criteria → 
beforeinstallprompt fires → usePWA captures event → 
InstallBanner shows → User clicks "Install Now" → 
Browser shows native install dialog → App installed!
```

### 2. **Offline Support**

```
User visits page → Service worker caches assets → 
User goes offline → Service worker serves from cache → 
App works offline!
```

### 3. **Install Banner Logic**

- Only shows if app is installable
- Hides if already installed
- Auto-dismisses for 7 days if user clicks "Maybe Later"
- Beautiful slide-up animation
- Mobile-responsive design

---

## 🧪 Testing

### Local Testing (Development)

1. **Build the app:**
```bash
cd /home/erpnext/frappe-bench/apps/shaadi/shaadi_ui
yarn build
```

2. **Open Chrome DevTools:**
   - Go to Application tab
   - Check Manifest section
   - Check Service Workers section
   - Run Lighthouse PWA audit

3. **Test Install Prompt:**
   - Open in Chrome
   - Look for install banner
   - Click "Install Now"
   - Verify app installs

### Mobile Testing

#### Android (Chrome):
1. Deploy to production (HTTPS required)
2. Open in Chrome mobile
3. Install banner should appear
4. Tap "Install Now"
5. App icon appears on home screen
6. Test offline functionality

#### iOS (Safari):
1. Deploy to production
2. Open in Safari
3. Tap Share button
4. Select "Add to Home Screen"
5. App icon appears on home screen
6. Test standalone mode

---

## 📊 PWA Checklist

### Essential Requirements:
- [x] HTTPS enabled on production
- [x] manifest.json created
- [x] Service worker implemented
- [x] PWA meta tags added
- [x] Install prompt implemented
- [ ] Icons generated (PNG from SVG)
- [ ] Lighthouse PWA score > 90

### iOS Specific:
- [x] apple-mobile-web-app-capable meta tag
- [x] apple-mobile-web-app-status-bar-style meta tag
- [x] apple-touch-icon links
- [ ] Splash screens (optional)

### Android Specific:
- [x] Maskable icons configuration
- [x] Theme color set
- [x] App shortcuts defined

---

## 🎯 User Experience Features

### Install Banner
- **Location**: Fixed bottom (mobile) / Bottom-left (desktop)
- **Timing**: Shows immediately when installable
- **Dismissal**: 7-day cooldown
- **Design**: Purple-pink gradient matching brand

### Shortcuts (Long-press app icon)
1. **Browse Profiles** → `/browse`
2. **My Matches** → `/matches`
3. **Messages** → `/messages`
4. **My Profile** → `/my-profile`

### Offline Fallback
- Cached pages work offline
- Service worker serves from cache
- Graceful degradation for API calls

---

## 📱 Install Prompt Best Practices (Implemented)

Based on Google's web.dev recommendations:

### ✅ Event Capture
```javascript
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault(); // Prevent default mini-infobar
  deferredPrompt = e;  // Save for later
  isInstallable = true; // Show custom UI
});
```

### ✅ Custom Trigger
```javascript
const install = async () => {
  deferredPrompt.prompt(); // Show browser dialog
  const { outcome } = await deferredPrompt.userChoice;
  // Track user choice for analytics
};
```

### ✅ Analytics Tracking
```javascript
if (outcome === 'accepted') {
  console.log('User accepted install');
} else if (outcome === 'dismissed') {
  console.log('User dismissed install');
}
```

### ✅ Display Mode Detection
```javascript
// Check if already installed
if (window.matchMedia('(display-mode: standalone)').matches) {
  isInstalled = true;
}
```

---

## 🔧 Deployment Steps

### 1. Generate Icons
```bash
# Use online tool or ImageMagick to generate all PNG sizes
# Upload to /shaadi_ui/public/icons/
```

### 2. Build Frontend
```bash
cd /home/erpnext/frappe-bench/apps/shaadi/shaadi_ui
yarn build
```

### 3. Commit Changes
```bash
git add .
git commit -m "Add PWA support with install prompt and offline functionality"
git push origin dev
```

### 4. Deploy to Production
```bash
# On production server
cd /home/erpnext/frappe-bench
git pull
bench build --app shaadi
bench restart
```

### 5. Verify HTTPS
- Ensure production site uses HTTPS
- PWA requires secure context

### 6. Test Installation
- Open site on mobile
- Verify install banner appears
- Test install flow
- Check offline functionality

---

## 📈 Analytics & Monitoring

### Track Install Events
```javascript
// In usePWA.js - already implemented
window.addEventListener('appinstalled', () => {
  console.log('PWA was installed');
  // Send to analytics
  gtag('event', 'pwa_install', {
    'event_category': 'engagement',
    'event_label': 'PWA Install'
  });
});
```

### Track Install Prompt Outcome
```javascript
const { outcome } = await deferredPrompt.userChoice;
// Send to analytics
gtag('event', 'pwa_install_prompt', {
  'event_category': 'engagement',
  'event_label': outcome
});
```

---

## 🐛 Troubleshooting

### Install Banner Not Showing?

**Check:**
1. HTTPS enabled?
2. Service worker registered?
3. Manifest.json valid?
4. Icons generated?
5. Already installed?
6. Browser supports PWA? (Chrome, Edge, Samsung Internet)

**Debug:**
```javascript
// Check in console
console.log('Is installable:', pwa.isInstallable);
console.log('Is installed:', pwa.isInstalled);
console.log('Deferred prompt:', pwa.deferredPrompt);
```

### Service Worker Not Registering?

**Check:**
1. HTTPS or localhost?
2. sw.js in public folder?
3. No JavaScript errors?
4. Check DevTools > Application > Service Workers

### iOS Not Installing?

**Note:** iOS only supports PWA install via Safari:
1. Open in Safari (not Chrome/Edge)
2. Tap Share button
3. Select "Add to Home Screen"
4. Chrome/Edge on iOS don't support PWA install

---

## 🎨 Customization

### Change Theme Color
Edit `manifest.json`:
```json
"theme_color": "#YOUR_COLOR"
```

### Change App Name
Edit `manifest.json`:
```json
"name": "Your App Name",
"short_name": "Short Name"
```

### Modify Install Banner
Edit `/shaadi_ui/src/components/InstallBanner.vue`:
- Change colors, text, layout
- Adjust timing, dismissal logic
- Add custom animations

### Update Shortcuts
Edit `manifest.json` shortcuts array:
```json
{
  "name": "New Shortcut",
  "url": "/your-route",
  "icons": [...]
}
```

---

## 📚 Resources

### Documentation
- **Google PWA Guide**: https://web.dev/progressive-web-apps/
- **MDN PWA**: https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps
- **Web App Manifest**: https://web.dev/add-manifest/
- **Service Workers**: https://web.dev/service-workers-cache-storage/

### Tools
- **PWA Builder**: https://www.pwabuilder.com/
- **Lighthouse**: Built into Chrome DevTools
- **Maskable.app**: https://maskable.app/

### Libraries
- **vue-pwa-install**: https://github.com/Bartozzz/vue-pwa-install
- **Workbox**: https://developers.google.com/web/tools/workbox

---

## ✨ What's Next?

### Phase 2 Enhancements:
1. **Push Notifications**
   - Request permission
   - Subscribe to push service
   - Send engagement notifications

2. **Background Sync**
   - Sync messages when back online
   - Queue failed API calls
   - Retry automatically

3. **Advanced Caching**
   - Cache API responses
   - Implement cache strategies
   - Precache critical routes

4. **Splash Screens**
   - Generate for all iOS devices
   - Improve launch experience
   - Match brand colors

5. **Share Target API**
   - Allow sharing to Shaadi app
   - Share profiles with friends
   - Improve engagement

---

## 🎉 Summary

Your Shaadi app now has:

✅ **Full PWA Support**
✅ **Custom Install Prompt**
✅ **Offline Functionality**
✅ **iOS & Android Compatible**
✅ **App Shortcuts**
✅ **Service Worker Caching**
✅ **Beautiful Install Banner**
✅ **Analytics Ready**

**Next Step:** Generate the PNG icons and deploy to production!
