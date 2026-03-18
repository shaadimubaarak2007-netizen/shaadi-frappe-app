#!/bin/bash

# PWA Icon Generator Script for Shaadi App
# This script converts the SVG icon to all required PNG sizes

echo "🎨 Generating PWA icons for Shaadi app..."

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "❌ ImageMagick is not installed!"
    echo "Install it with: sudo apt-get install imagemagick"
    exit 1
fi

# Navigate to icons directory
cd "$(dirname "$0")/shaadi_ui/public/icons" || exit

# Check if source SVG exists
if [ ! -f "icon-source.svg" ]; then
    echo "❌ icon-source.svg not found!"
    exit 1
fi

echo "📁 Source: icon-source.svg"
echo "📍 Output directory: $(pwd)"
echo ""

# Generate all required icon sizes
sizes=(16 32 72 96 128 144 152 180 192 384 512)

for size in "${sizes[@]}"; do
    output="icon-${size}x${size}.png"
    echo "⚙️  Generating ${output}..."
    convert icon-source.svg -resize ${size}x${size} "$output"
    
    if [ $? -eq 0 ]; then
        echo "✅ ${output} created"
    else
        echo "❌ Failed to create ${output}"
    fi
done

echo ""
echo "🎉 Icon generation complete!"
echo ""
echo "📊 Generated icons:"
ls -lh icon-*.png | awk '{print "   " $9 " - " $5}'

echo ""
echo "✅ All PWA icons are ready!"
echo "Next steps:"
echo "  1. Run 'yarn build' to build the app"
echo "  2. Deploy to production with HTTPS"
echo "  3. Test PWA installation on mobile devices"
