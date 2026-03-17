#!/bin/bash
# Fix production build by installing unplugin-icons dependencies

echo "Installing unplugin-icons and icon sets..."
cd /home/erpnext/frappe-bench/apps/shaadi/shaadi_ui

# Install required packages
yarn add -D unplugin-icons @iconify/json

echo "Dependencies installed successfully!"
echo "Now update vite.config.js to include the unplugin-icons plugin"
