
import yt_dlp
import os

async def download_media(client, message, url):
    await message.reply_text("Downloading Facebook video...")
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
    await message.reply_document(filepath, caption=f"Downloaded Facebook video: {info['title']}")
