
import yt_dlp
import os

async def download_song(client, message, query):
    await message.reply_text(f"Searching and downloading song: {query}")
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        filepath = ydl.prepare_filename(info['entries'][0])
    await message.reply_document(filepath, caption=f"Downloaded song: {info['entries'][0]['title']}")

async def download_video(client, message, query):
    await message.reply_text(f"Searching and downloading video: {query}")
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {'format': 'best', 'outtmpl': 'downloads/%(title)s.%(ext)s'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        filepath = ydl.prepare_filename(info['entries'][0])
    await message.reply_document(filepath, caption=f"Downloaded video: {info['entries'][0]['title']}")
