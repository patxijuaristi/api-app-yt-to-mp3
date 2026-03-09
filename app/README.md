# YouTube to MP3 - Flutter App

A cross-platform Flutter application to convert YouTube videos to MP3 audio files.

## Features

- Search YouTube videos by URL
- Preview video information (title, author, thumbnail, duration)
- Download videos as MP3 audio files
- Track download progress
- Modern Material 3 UI design

## Screenshots

*Coming soon*

## Requirements

- Flutter 3.x
- Dart SDK >=3.0.0
- Running backend API (see `../api/`)

## Installation

1. **Install dependencies:**
   ```bash
   flutter pub get
   ```

2. **Configure environment:**
   
   Create a `.env` file in the app root:
   ```
   API_BASE_URL=http://localhost:8000
   ```

3. **Generate app icons (optional):**
   ```bash
   dart run flutter_launcher_icons
   ```

4. **Run the app:**
   ```bash
   flutter run
   ```

## Supported Platforms

- Android
- iOS
- Web
- Windows
- macOS
- Linux

## Project Structure

```
lib/
├── main.dart              # App entry point
├── models/
│   └── video_model.dart   # Video data model
├── screens/
│   └── home_screen.dart   # Main screen UI
└── services/
    └── api_service.dart   # API communication
```

## Dependencies

- `http` - HTTP requests
- `path_provider` - File system access
- `permission_handler` - Runtime permissions
- `url_launcher` - Open external URLs
- `flutter_dotenv` - Environment variables

## Configuration

The app uses environment variables for configuration. Create a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API URL | `http://localhost:8000` |

## Building for Production

### Android
```bash
flutter build apk --release
```

### iOS
```bash
flutter build ios --release
```

### Web
```bash
flutter build web --release
```

### Windows
```bash
flutter build windows --release
```

## Author

Developed by [Patxi Juaristi](https://juaristech.com)

## License

MIT
