from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent
PAPER_DIR = BASE_DIR / "papers"
PROMPT_TEMPLATE_DIR = BASE_DIR / "prompt_templates"

MODELS = [
    "gpt-oss-120b",
    "mistral-large-3-675b-instruct-2512",
    "qwen3.5-397b-a17b"
]
MODEL_NAMES = "_".join(MODELS)
OUTPUT_PATH = BASE_DIR / "data" / f"{MODEL_NAMES}.json"
OUTPUT_CSV_PATH = BASE_DIR / "data" / f"{MODEL_NAMES}.csv"
OUTPUT_HTML_PATH = BASE_DIR / "data" / f"{MODEL_NAMES}.html"

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://chat-ai.academiccloud.de/v1"