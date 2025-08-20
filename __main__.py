from pyrogram import Client
from dotenv import load_dotenv
import os

plugins = dict(root="plugins")
load_dotenv()
API_ID = os.getenv("API_id")
API_HASH = os.getenv("API_HASH")
TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "my_account", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, plugins=plugins
)

app.run()
