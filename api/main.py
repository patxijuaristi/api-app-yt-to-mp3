import os
import uuid
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import yt_dlp

app = FastAPI(
    title="YouTube to MP3 API",
    description="Simple API to convert YouTube videos to MP3",
    version="1.0.0"
)


@app.get("/convert")
async def convert_to_mp3(url: str):
    """
    Converts a YouTube video to MP3 and returns it to the user.
    
    - **url**: YouTube video URL as query param
    
    Example: /convert?url=https://www.youtube.com/watch?v=VIDEO_ID
    """
    
    # Create temporary directory for files
    temp_dir = tempfile.gettempdir()
    unique_id = str(uuid.uuid4())
    output_path = os.path.join(temp_dir, f"{unique_id}")
    
    # yt-dlp configuration to extract audio only in MP3 format
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        # Download and convert the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video information first
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'audio')
            
            # Download the video
            ydl.download([url])
        
        # The generated MP3 file
        mp3_file = f"{output_path}.mp3"
        
        if not os.path.exists(mp3_file):
            raise HTTPException(status_code=500, detail="Error generating MP3 file")
        
        # Clean the filename for the user
        safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{safe_title}.mp3"
        
        return FileResponse(
            path=mp3_file,
            filename=filename,
            media_type="audio/mpeg",
            background=None  # The file will be deleted after sending
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
        "usage": "GET /convert?url=YOUTUBE_URL",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
