import os
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules import youtube, tiktok, instagram, facebook, search
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("multi_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

START_TEXT = "👋 Hello! I am a **Multi Social Media Downloader Bot**.\n\nSend me links from YouTube, TikTok, Instagram, Facebook or use /song and /video commands to download content."

HELP_TEXT = "**Bot Commands:**\n/start - Start the bot\n/song <song name> - Download audio from YouTube\n/video <video name> - Download video from YouTube\nSend any supported social media link to download videos."

INLINE_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("Developer @deweni2", url="https://t.me/deweni2")],
    [InlineKeyboardButton("Support Group @slmusicmania", url="https://t.me/slmusicmania")],
    [InlineKeyboardButton("Help / Commands", callback_data="help_cmd")]
])

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(START_TEXT, reply_markup=INLINE_BUTTONS)

@app.on_callback_query()
async def callback(client, callback_query):
    data = callback_query.data

    # Help button
    if data == "help_cmd":
        await callback_query.message.edit(HELP_TEXT, reply_markup=INLINE_BUTTONS)
        return

    # YouTube download buttons
    if data.startswith(("yt_video", "yt_audio")):
        action, url, user_id = data.split("|")
        if str(callback_query.from_user.id) != user_id:
            return await callback_query.answer("❌ This button is not for you.", show_alert=True)

        await callback_query.answer()
        await callback_query.message.edit("⏳ Downloading...")

        os.makedirs("downloads", exist_ok=True)
        ydl_opts = {'outtmpl': 'downloads/%(title)s.%(ext)s'}
        if action == "yt_video":
            ydl_opts['format'] = 'best'
        else:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)
                if action == "yt_audio":
                    filepath = os.path.splitext(filepath)[0] + ".mp3"

            meta = f"**Title:** {info.get('title')}\n"
            meta += f"**Uploader:** {info.get('uploader')}\n"
            meta += f"**Views:** {info.get('view_count')}\n"
            meta += f"**Duration:** {info.get('duration')} sec\n"
            meta += f"\nRequested by: [{callback_query.from_user.first_name}](tg://user?id={callback_query.from_user.id})"

            await client.send_document(
                chat_id=callback_query.message.chat.id,
                document=filepath,
                caption=meta
            )
            os.remove(filepath)
            await callback_query.message.delete()

        except Exception as e:
            await client.send_message(callback_query.message.chat.id, f"❌ Error: {e}")

@app.on_message(filters.text & filters.private)
async def downloader(client, message):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        buttons = youtube.get_buttons(url, message.from_user.id)
        await message.reply_text("Choose download option:", reply_markup=buttons)
    elif "tiktok.com" in url:
        await tiktok.download_video(client, message, url)
    elif "instagram.com" in url:
        await instagram.download_media(client, message, url)
    elif "facebook.com" in url or "fb.watch" in url:
        await facebook.download_media(client, message, url)
    else:
        await message.reply_text("❌ Unsupported link or format.")

@app.on_message(filters.command("song") & filters.private)
async def song_search(client, message):
    query = message.text.split("/song ",1)[1]
    await search.download_song(client, message, query)

@app.on_message(filters.command("video") & filters.private)
async def video_search(client, message):
    query = message.text.split("/video ",1)[1]
    await search.download_video(client, message, query)

app.run()
