from dotenv import load_dotenv
import os

load_dotenv()  # فایل .env رو لود می‌کنه

DB_URL = os.getenv("DB_URL")
