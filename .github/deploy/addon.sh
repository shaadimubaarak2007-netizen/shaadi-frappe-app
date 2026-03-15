#!/bin/bash

# Custom deployment script for Shaadi app
# This script will be executed after the default deployment

echo "🚀 Starting Shaadi app specific deployment..."

# Build frontend assets
echo "📦 Building frontend assets..."
cd $DEPLOY_PATH/apps/shaadi/shaadi_ui
npm install
npm run build

# Sync built assets to Frappe public folder
echo "🔄 Syncing frontend assets..."
cd $DEPLOY_PATH
cp -r apps/shaadi/shaadi/shaadi/public/* sites/$SITE_NAME/public/assets/
cp apps/shaadi/shaadi/shaadi/www/frontend.html sites/$SITE_NAME/public/

# Run Shaadi-specific migrations
echo "🔧 Running Shaadi app migrations..."
cd $DEPLOY_PATH
bench --site $SITE_NAME migrate

# Build JS and CSS for Shaadi app
echo "🎨 Building JS and CSS..."
cd $DEPLOY_PATH
bench build --app shaadi

# Restart services
echo "🔄 Restarting services..."
bench restart

# Clear cache
echo "🧹 Clearing cache..."
bench --site $SITE_NAME clear-cache

echo "✅ Shaadi app deployment completed successfully!"
echo "🌐 Site: https://$SITE_NAME"
