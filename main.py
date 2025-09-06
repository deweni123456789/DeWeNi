import os
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
    if callback_query.data == "help_cmd":
        await callback_query.message.edit(HELP_TEXT, reply_markup=INLINE_BUTTONS)

@app.on_message(filters.text & filters.private)
async def downloader(client, message):
    url = message.text.strip()
    if "youtube.com" in url or "youtu.be" in url:
        await youtube.download_video(client, message, url)
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
