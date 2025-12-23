#!/bin/bash
# Start Frontend Server

cd "$(dirname "$0")"
cd ../web

echo "🎨 Starting React Frontend..."
npm run dev
