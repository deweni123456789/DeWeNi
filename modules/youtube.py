import yt_dlp
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Track which callbacks are already registered
callback_registered = False

async def download_video(client, message, url):
    global callback_registered

    # Ensure downloads folder exists
    os.makedirs("downloads", exist_ok=True)

    # Create inline buttons for video/audio download
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Download Video", callback_data=f"yt_video|{url}|{message.from_user.id}")],
        [InlineKeyboardButton("Download Audio", callback_data=f"yt_audio|{url}|{message.from_user.id}")],
        [InlineKeyboardButton("Developer @deweni2", url="https://t.me/deweni2")]
    ])

    # Ask user to choose download option
    prompt = await message.reply_text("Choose download option:", reply_markup=buttons)

    if not callback_registered:
        # Register callback query handler only once
        @client.on_callback_query()
        async def callback(client, callback_query):
            data = callback_query.data
            if not data.startswith(("yt_video", "yt_audio")):
                return

            action, video_url, requester_id = data.split("|")
            if str(callback_query.from_user.id) != requester_id:
                await callback_query.answer("❌ This button is not for you.", show_alert=True)
                return

            await callback_query.answer()  # Stop loading

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
                # Download the file
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    filepath = ydl.prepare_filename(info)
                    if action == "yt_audio":
                        filepath = os.path.splitext(filepath)[0] + ".mp3"

                # Prepare metadata
                meta = f"**Title:** {info.get('title')}\n"
                meta += f"**Uploader:** {info.get('uploader')}\n"
                meta += f"**Upload Date:** {info.get('upload_date')}\n"
                meta += f"**Views:** {info.get('view_count')}\n"
                meta += f"**Likes:** {info.get('like_count')}\n"
                meta += f"**Comments:** {info.get('comment_count')}\n"
                meta += f"**Duration:** {info.get('duration')} seconds\n"
                meta += f"\nRequested by: [{callback_query.from_user.first_name}](tg://user?id={callback_query.from_user.id})"

                # Send document safely
                async with client.send_document(
                    chat_id=callback_query.message.chat.id,
                    document=filepath,
                    caption=meta
                ) as sent_msg:
                    pass

                # Delete downloaded file after sending
                os.remove(filepath)

            except Exception as e:
                await client.send_message(callback_query.message.chat.id, f"❌ Error: {e}")

        callback_registered = True

    # Clean the choose-option message after 60 seconds if user didn't press
    await prompt.delete(True)
