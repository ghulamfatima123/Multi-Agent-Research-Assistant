import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Free API keys (optional)
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # URLs
    SERPER_URL = "https://google.serper.dev/search"
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    # Settings
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    SUMMARY_MAX_LENGTH = int(os.getenv("SUMMARY_MAX_LENGTH", "300"))
    REQUEST_TIMEOUT = 15

config = Config()