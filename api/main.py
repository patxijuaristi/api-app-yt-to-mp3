import os
import glob
import uuid
import shutil
import tempfile
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
import yt_dlp

app = FastAPI(
    title="YouTube to MP3 API",
    description="API to download audio from YouTube videos",
    version="1.0.0"
)

# Check if FFmpeg is available
FFMPEG_AVAILABLE = shutil.which('ffmpeg') is not None


@app.get("/convert")
async def convert_to_audio(
    url: str,
    format: str = Query(default="auto", description="Output format: mp3, m4a, or auto (mp3 if FFmpeg available, otherwise native)")
):
    """
    Downloads audio from a YouTube video.
    
    - **url**: YouTube video URL
    - **format**: Output format (mp3, m4a, auto)
    
    Example: /convert?url=https://www.youtube.com/watch?v=VIDEO_ID&format=mp3
    """
    
    # Determine output format
    use_mp3 = format == "mp3" or (format == "auto" and FFMPEG_AVAILABLE)
    
    if use_mp3 and not FFMPEG_AVAILABLE:
        raise HTTPException(
            status_code=400, 
            detail="MP3 conversion requires FFmpeg which is not installed. Use format=m4a instead."
        )
    
    # Create temporary directory for files
    temp_dir = tempfile.gettempdir()
    unique_id = str(uuid.uuid4())
    output_path = os.path.join(temp_dir, unique_id)
    
    # yt-dlp configuration
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path + '.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # Avoid YouTube bot detection
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'web'],
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
    }
    
    # Add MP3 conversion if requested and FFmpeg available
    if use_mp3:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    try:
        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get('title', 'audio')
        
        # Find the downloaded file
        if use_mp3:
            audio_file = f"{output_path}.mp3"
            media_type = "audio/mpeg"
            ext = "mp3"
        else:
            # Find the actual downloaded file (could be .m4a, .webm, .opus, etc.)
            files = glob.glob(f"{output_path}.*")
            if not files:
                raise HTTPException(status_code=500, detail="Error: audio file not found")
            audio_file = files[0]
            ext = os.path.splitext(audio_file)[1][1:]  # Get extension without dot
            media_types = {
                'm4a': 'audio/mp4',
                'webm': 'audio/webm', 
                'opus': 'audio/opus',
                'ogg': 'audio/ogg',
            }
            media_type = media_types.get(ext, 'audio/mpeg')
        
        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Error generating audio file")
        
        # Clean the filename for the user
        safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{safe_title}.{ext}"
        
        return FileResponse(
            path=audio_file,
            filename=filename,
            media_type=media_type,
        )
        
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=400, detail=f"Error downloading video: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/")
async def root():
    """Welcome endpoint with usage information."""
    return {
        "message": "YouTube to MP3 API",
        "usage": "GET /convert?url=YOUTUBE_URL&format=auto",
        "formats": ["mp3", "m4a", "auto"],
        "ffmpeg_available": FFMPEG_AVAILABLE,
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
