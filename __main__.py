from pyrogram import Client
from dotenv import load_dotenv
from app.core.init_db import init_db
import os
import asyncio


plugins = dict(root="plugins")
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TOKEN = os.getenv("BOT_TOKEN")


async def main():
    await init_db()
    app = Client(
        "my_account", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, plugins=plugins
    )
    await app.start()
    await app.idle()


asyncio.run(main())
