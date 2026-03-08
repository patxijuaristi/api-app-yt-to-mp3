# YouTube to MP3 API

Simple API with FastAPI to convert YouTube videos to MP3.

## Requirements

- Python 3.8+
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

```bash
pip install -r requirements.txt
```

## Usage

### Start the server

```bash
python main.py
```

The server will run at `http://localhost:8000`

### Endpoint

```
GET /convert?url={YOUTUBE_URL}
```

### Example

```
http://localhost:8000/convert?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Interactive documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project structure

```
api-yt-mp3/
├── main.py          # FastAPI API
├── requirements.txt # Dependencies
└── README.md        # This file
```

## Dependencies

- **FastAPI** - Web framework
- **uvicorn** - ASGI server
- **yt-dlp** - YouTube video download
