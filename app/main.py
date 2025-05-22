from fastapi import FastAPI
from app.api.services.news_fetcher import get_sources

app = FastAPI(
    title="NewsFudge",
    version="0.1.0",
    description="Fast API AI APP"
)

@app.get("/")
def root():
    return {"message":"Welcome to News Fudge"}

@app.get("/sources")
async def sources():
    return await get_sources()




