import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPEN_ROUTER_KEY = os.getenv("OPEN_ROUTER_KEY")
GEMINI_MODEL = "gemma-4-31b-it"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAPER_DIR = os.path.join(BASE_DIR, "data", "papers")
DB_DIR = os.path.join(BASE_DIR, "data", "chromadb")
SUMMARY_DIR = os.path.join(BASE_DIR, "summaries")

os.makedirs(PAPER_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(SUMMARY_DIR, exist_ok=True)