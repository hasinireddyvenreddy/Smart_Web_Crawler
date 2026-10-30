
import os
from pathlib import Path
from dotenv import load_dotenv

# Project base directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Website crawling settings
MAX_DEPTH = int(os.getenv("MAX_DEPTH", 2))
MAX_PAGES = int(os.getenv("MAX_PAGES", 10))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 15))
REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", 1))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

# User agent
USER_AGENT = os.getenv(
    "USER_AGENT",
    "SmartWebCrawler/1.0"
)

# Folder paths
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

# Create folders if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Export file paths
JSON_FILE = OUTPUT_DIR / "data.json"
CSV_FILE = OUTPUT_DIR / "data.csv"

# Log file path
LOG_FILE = LOGS_DIR / "crawler.log"
