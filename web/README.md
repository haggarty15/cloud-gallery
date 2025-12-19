# Web Gallery

React-based web gallery for the Cloud Gallery Portfolio system.

## Overview

Public-facing web gallery that displays approved images with an admin dashboard for image approval.

## Features

- **Public Gallery**: Responsive grid of approved images
- **Image Details**: Modal view with full image and metadata
- **Admin Dashboard**: Review and approve/reject pending images
- **Authentication**: Firebase authentication for admin access
- **Responsive Design**: Mobile-first, works on all devices

## Technology Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: CSS Modules + Tailwind CSS
- **Authentication**: Firebase SDK
- **HTTP Client**: Axios
- **Routing**: React Router
- **State Management**: React Context API

## Directory Structure

```
web/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── Gallery.jsx
│   │   ├── ImageCard.jsx
│   │   ├── ImageModal.jsx
│   │   ├── AdminDashboard.jsx
│   │   ├── Header.jsx
│   │   └── Login.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── firebase.js
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── .env.example
├── package.json
├── vite.config.js
└── README.md
```

## Setup

### Prerequisites

- Node.js 18+ and npm
- Firebase project configured

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## Environment Variables

```bash
VITE_API_URL=https://gallery-backend-xxx.run.app
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

## Development

```bash
# Start dev server
npm run dev

# Run linter
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

## Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

### Cloud Run

```bash
# Build and deploy
gcloud run deploy gallery-web \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Firebase Hosting

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting

# Build
npm run build

# Deploy
firebase deploy --only hosting
```

### Static Hosting

The build output in `dist/` can be deployed to any static hosting service:
- Cloud Storage + Cloud CDN
- Netlify
- Vercel
- GitHub Pages

## Features Detail

### Public Gallery

- Grid layout of approved images
- Lazy loading for performance
- Infinite scroll pagination
- Click to view full image
- Responsive design

### Image Modal

- Full-size image display
- Image metadata (title, description, uploader)
- Swipe/keyboard navigation
- Close on overlay click

### Admin Dashboard

- Login required
- List of pending images
- Approve/reject actions
- Image preview
- Rejection reason input

### Authentication

- Firebase email/password authentication
- Google Sign-In option
- Protected admin routes
- Automatic token refresh

## Components

### Gallery

Main gallery component that fetches and displays approved images in a grid layout.

### ImageCard

Individual image card component with thumbnail and metadata.

### ImageModal

Modal overlay for viewing full-size images with navigation.

### AdminDashboard

Protected admin interface for reviewing and approving images.

### Header

Navigation header with auth status and admin link.

### Login

Authentication form with Firebase integration.

## API Integration

All API calls go through `src/services/api.js`:

```javascript
import { getGallery, uploadImage, approveImage } from './services/api';

// Get gallery images
const images = await getGallery(page, limit);

// Upload image (requires auth)
const result = await uploadImage(file, token);

// Approve image (admin only)
await approveImage(imageId, token);
```

## Styling

- Tailwind CSS for utility classes
- CSS Modules for component-specific styles
- Mobile-first responsive design
- Dark mode support (optional)

## Performance

- Code splitting per route
- Lazy loading images
- Optimized bundle size
- Service worker for caching (PWA)

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome)

## Testing

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

## Troubleshooting

### API Connection Issues
- Verify API_URL is correct in .env
- Check CORS configuration on backend
- Ensure API is deployed and accessible

### Firebase Auth Issues
- Verify Firebase config in .env
- Check Firebase console for auth settings
- Ensure web app is registered in Firebase

### Build Issues
- Clear node_modules and reinstall
- Check Node.js version (18+)
- Verify all env variables are set

## Future Enhancements

- [ ] Search functionality
- [ ] Filter by uploader
- [ ] Sort options
- [ ] User profiles
- [ ] Image likes/favorites
- [ ] Comments
- [ ] Share buttons
- [ ] Progressive Web App (PWA)
- [ ] Offline support
- [ ] Dark mode toggle
