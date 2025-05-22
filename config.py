import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"
DATASET_PATH = "freelancer_earnings_bd.csv"
LOG_FILE = "logs.jsonl"

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в .env файле.")
