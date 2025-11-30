from pyrogram import Client, filters
import asyncio
from pyrogram.types import Message

# --- ENV VARIABLES (Railway) ---
import os
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

SOURCE_ID = int(os.getenv("SOURCE_ID"))     # channel/group you COPY FROM
DEST_ID = int(os.getenv("DEST_ID"))         # channel you POST TO

# --- Affiliate Converter Bot ---
CONVERTER_BOT = "ek10convertbot"  # EarnKaro 10 bot username

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Helper: Convert text using EarnKaro 10 Bot ---
async def convert_affiliate(text: str) -> str:
    try:
        # send message to converter bot
        msg = await app.send_message(CONVERTER_BOT, text)
        await asyncio.sleep(2)

        # wait for reply from converter bot
        async for m in app.get_dialog_history(CONVERTER_BOT, limit=1):
            if m.reply_to_message and m.reply_to_message.id == msg.id:
                return m.text
        return text
    except:
        return text


# --- Listener: When message arrives in the source channel ---
@app.on_message(filters.chat(SOURCE_ID))
async def repost_handler(_, message: Message):

    # Extract text or caption
    content = message.text or message.caption or ""

    # Convert affiliate links
    converted = await convert_affiliate(content)

    # If photo
    if message.photo:
        await app.send_photo(
            DEST_ID,
            photo=message.photo.file_id,
            caption=converted
        )

    # If video
    elif message.video:
        await app.send_video(
            DEST_ID,
            video=message.video.file_id,
            caption=converted
        )

    # If text only
    elif message.text:
        await app.send_message(
            DEST_ID,
            converted
        )


print("Bot started successfully…")
app.run()
