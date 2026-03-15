#!/bin/bash

# Sync built frontend assets to Frappe sites folder
# Run this after building the frontend with yarn build

echo "🔄 Syncing Shaadi frontend assets to Frappe..."

# Copy assets from build output to sites/assets
cp -r apps/shaadi/shaadi/shaadi/public/* sites/assets/shaadi/

echo "✅ Assets synced successfully!"
echo "📁 Assets location: sites/assets/shaadi/"
echo ""
echo "🧹 Clearing cache..."
bench --site shaadi.localhost clear-cache

echo "✅ Done! Frontend ready at http://localhost:8000/frontend"
