# YouTube to MP3 API

Backend API built with FastAPI to convert YouTube videos to MP3 audio files.

> **Important:** This API must be deployed and accessible for the [Flutter app](../app/) to work. The app connects to this API to perform video conversions.

## Requirements

- Python 3.10+
- FFmpeg installed on the system

### Install FFmpeg

**Windows:**
```bash
winget install ffmpeg
```
Or download from: https://ffmpeg.org/download.html

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

## Installation

1. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Local Development

Start the server:
```bash
python main.py
```

The server will run at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and usage |
| GET | `/convert?url={URL}` | Convert YouTube video to MP3 |

### Example

```
GET http://localhost:8000/convert?url=https://www.youtube.com/watch?v=VIDEO_ID
```

### Interactive Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### cPanel (with Passenger)

The API includes `passenger_wsgi.py` for WSGI compatibility.

1. Create a Python App in cPanel (Python 3.10+)
2. Upload all files to the application root
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure:
   - **Application startup file:** `passenger_wsgi.py`
   - **Application Entry point:** `application`

5. Restart the application

> **Note:** Ensure FFmpeg is installed on the server. Contact your hosting provider if it's not available.

### Docker

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Other Platforms

- **Railway/Render:** Deploy directly from GitHub
- **VPS:** Use systemd + nginx + uvicorn
- **AWS/GCP/Azure:** Use their container or serverless services

## Connecting the Flutter App

Once deployed, update the Flutter app's `.env` file:

```env
API_BASE_URL=https://your-api-domain.com
```

## Project Structure

```
api/
├── main.py              # FastAPI application
├── passenger_wsgi.py    # WSGI adapter for cPanel
├── requirements.txt     # Python dependencies
└── README.md
```

## Dependencies

- **FastAPI** - Modern web framework
- **uvicorn** - ASGI server
- **yt-dlp** - YouTube video/audio download
- **a2wsgi** - ASGI to WSGI adapter

## Author

Developed by [Patxi Juaristi](https://juaristech.com)

## License

MIT
