import os
from dotenv import load_dotenv

# Загружаем переменные из .env при старте проекта
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
