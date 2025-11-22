# ALGSOCH Mobile App

React Native mobile application for ALGSOCH portfolio platform.

## Setup

### Prerequisites
- Node.js 18+
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac only) or Android Studio

### Installation

```bash
cd mobile-app
npm install
```

### Run Development

```bash
# Start Expo dev server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android

# Run in web browser
npm run web
```

### Build for Production

```bash
# Build for iOS
expo build:ios

# Build for Android
expo build:android
```

## Features

- ✅ Home screen with portfolio overview
- ✅ Projects list with details
- ✅ Skills showcase
- ✅ Timeline (education & experience)
- ✅ Contact form
- ✅ Dark/light theme support
- ✅ Offline fallback
- ✅ WebSocket real-time updates
- ✅ SSE event stream

## API Configuration

Update API URLs in `app.json`:

```json
{
  "extra": {
    "apiUrl": "https://your-api.com",
    "analyticsApiUrl": "https://your-analytics.com",
    "wsUrl": "wss://your-api.com"
  }
}
```

## Project Structure

```
mobile-app/
├── src/
│   ├── screens/       # Screen components
│   ├── components/    # Reusable components
│   ├── services/      # API services
│   ├── hooks/         # Custom hooks
│   └── utils/         # Utilities
├── assets/            # Images, fonts
├── App.tsx            # Root component
└── app.json           # Expo configuration
```

## Tech Stack

- React Native
- Expo
- TypeScript
- React Navigation
- Axios
- AsyncStorage
