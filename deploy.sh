#!/bin/bash

# Deploy MkDocs site to GitHub Pages
# Usage: ./deploy.sh

echo "🚀 Building MkDocs site..."

# Build the site
mkdocs build --clean

echo "📦 Site built successfully!"
echo "📁 Files are in ./site directory"
echo ""
echo "To deploy to GitHub Pages:"
echo "1. Push to main branch (auto-deploy via GitHub Actions)"
echo "2. Or manually: gh-pages branch deployment"
echo ""
echo "🌐 Site will be available at:"
echo "https://mtalvik.github.io/automatiseerimine_ext"
