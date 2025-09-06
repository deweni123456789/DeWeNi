
from pyrogram import types
import requests
import os

async def download_video(client, message, url):
    await message.reply_text("Downloading TikTok video...")
    os.makedirs('downloads', exist_ok=True)
    import yt_dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
    await message.reply_document(filepath, caption=f"Downloaded TikTok video: {info['title']}")
