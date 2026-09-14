import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (weather_bot/.env)
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

BOT_TOKEN: str | None = os.getenv("BOT_TOKEN")
WEATHER_API_KEY: str | None = os.getenv("WEATHER_API_KEY")
WEATHER_API_BASE_URL: str = "https://api.weatherapi.com/v1/current.json"

# Database path
DATA_DIR = BASE_DIR / "data"
DB_PATH: str = str(DATA_DIR / "weather_bot.db")

# Validation is done at startup in main.py for better error messages
