#!/usr/bin/env node

/**
 * Post-build script to clean up shaadi.html
 * Removes the problematic script block added by jinjaBootData plugin
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const htmlPath = path.join(__dirname, '../../shaadi/www/shaadi.html');

console.log('Cleaning up shaadi.html...');

try {
    let html = fs.readFileSync(htmlPath, 'utf8');
    
    // Remove the problematic script block that jinjaBootData adds
    // This block causes TypeError because it tries to use tojson on LocalProxy
    const problematicBlock = /\s*<script>\s*{% for key in boot %}[\s\S]*?{% endfor %}\s*<\/script>\s*/g;
    
    html = html.replace(problematicBlock, '');
    
    // Fix double slashes in asset paths
    html = html.replace(/\/assets\/shaadi\/\//g, '/assets/shaadi/');
    
    fs.writeFileSync(htmlPath, html, 'utf8');
    
    console.log('✓ Successfully cleaned up shaadi.html');
} catch (error) {
    console.error('Error cleaning up shaadi.html:', error.message);
    process.exit(1);
}
