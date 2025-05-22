from dotenv import load_dotenv
import os

load_dotenv()
NEWS_API_URL= os.getenv("NEWS_API_URL")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "us")
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "technology")