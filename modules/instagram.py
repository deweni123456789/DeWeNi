
import instaloader
import os

async def download_media(client, message, url):
    await message.reply_text("Downloading Instagram media...")
    os.makedirs('downloads', exist_ok=True)
    L = instaloader.Instaloader(dirname_pattern='downloads')
    try:
        post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])
        L.download_post(post, target=post.owner_username)
        await message.reply_text(f"Downloaded Instagram media from {url}")
    except Exception as e:
        await message.reply_text(f"Error downloading Instagram media: {e}")
