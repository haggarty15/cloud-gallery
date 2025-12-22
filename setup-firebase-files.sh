#!/bin/bash
# Helper script to complete Firebase setup after browser configuration
# Run this AFTER you've downloaded google-services.json and firebase-admin-key.json

set -e  # Exit on error

echo "🔥 Firebase Setup Helper Script"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if files were downloaded
echo "📥 Checking for downloaded files..."
echo ""

# Check google-services.json
if [ -f "$HOME/Downloads/google-services.json" ]; then
    echo -e "${GREEN}✓${NC} Found google-services.json in Downloads"
    echo "  Moving to android/app/..."
    mv "$HOME/Downloads/google-services.json" android/app/google-services.json
    echo -e "${GREEN}✓${NC} Moved successfully"
else
    echo -e "${YELLOW}⚠${NC} google-services.json not found in Downloads"
    echo "  Please download it from Firebase Console"
fi

echo ""

# Check firebase admin key
ADMIN_KEY=$(find "$HOME/Downloads" -name "image-gallery-481812-firebase-adminsdk-*.json" 2>/dev/null | head -n 1)
if [ -n "$ADMIN_KEY" ]; then
    echo -e "${GREEN}✓${NC} Found Firebase Admin key in Downloads"
    echo "  Moving to backend/firebase-admin-key.json..."
    mv "$ADMIN_KEY" backend/firebase-admin-key.json
    echo -e "${GREEN}✓${NC} Moved successfully"
else
    echo -e "${YELLOW}⚠${NC} Firebase Admin key not found in Downloads"
    echo "  Please download it from Firebase Console > Service Accounts"
fi

echo ""
echo "================================"
echo ""

# Verify files are in place
echo "🔍 Verifying file placement..."
echo ""

MISSING=0

if [ -f "android/app/google-services.json" ]; then
    echo -e "${GREEN}✓${NC} android/app/google-services.json"
else
    echo -e "${RED}✗${NC} android/app/google-services.json (MISSING)"
    MISSING=1
fi

if [ -f "backend/firebase-admin-key.json" ]; then
    echo -e "${GREEN}✓${NC} backend/firebase-admin-key.json"
else
    echo -e "${RED}✗${NC} backend/firebase-admin-key.json (MISSING)"
    MISSING=1
fi

echo ""

if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✓ All Firebase credential files in place!${NC}"
    echo ""
    echo "📝 Next step: Update web/.env with Firebase config"
    echo ""
    echo "Run this command and paste your Firebase config values:"
    echo "  nano web/.env"
    echo ""
    echo "Or I can help you update it in the next step."
else
    echo -e "${RED}✗ Some files are missing${NC}"
    echo ""
    echo "Please complete the Firebase Console steps first:"
    echo "1. Download google-services.json from Android app settings"
    echo "2. Download Firebase Admin key from Service Accounts"
    echo "3. Run this script again"
fi

echo ""
echo "================================"
