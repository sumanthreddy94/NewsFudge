from dotenv import load_dotenv
import os

load_dotenv()
NEWS_API= os.getenv("NEWS_API")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "us")
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "technology")