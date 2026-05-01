from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent
PAPER_DIR = BASE_DIR / "papers"
PROMPT_TEMPLATE_DIR = BASE_DIR / "prompt_templates"

MODELS = [
    "gpt-oss-120b",
    "deepseek-r1-distill-llama-70b",
    "qwen3-30b-a3b-instruct-2507"
]
MODEL_NAMES = "_".join(MODELS)
OUTPUT_PATH = BASE_DIR / "data" / f"{MODEL_NAMES}.json"
OUTPUT_CSV_PATH = BASE_DIR / "data" / f"{MODEL_NAMES}.csv"
OUTPUT_HTML_PATH = BASE_DIR / "data" / f"{MODEL_NAMES}.html"

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://chat-ai.academiccloud.de/v1"