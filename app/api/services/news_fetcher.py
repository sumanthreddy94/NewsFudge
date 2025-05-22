import datetime
import httpx

from app.core.config import NEWS_API_URL, NEWS_API_KEY

from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key = NEWS_API_KEY)

# Not To Use
async def get_sources():
    if not NEWS_API_KEY:
        return {"error": "Missing NEWS_API_KEY in environment."}
    
    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NEWS_API_URL+ '/top-headlines/sources', headers = headers)
            response.raise_for_status() 
            return response.json()
        except httpx.HTTPError as err:
            return {"error": str(err)}
        
async def fetch_top_headlines(
    q: str = None,
    sources: str = None,
    category: str = None,
    language: str = "en",
    country: str = "us"
):
    return newsapi.get_top_headlines(
        q=q,
        sources=sources,
        category=category,
        language=language,
        country=country
    )

# /v2/everything
async def fetch_everything(
    q: str,
    sources: str = None,
    domains: str = None,
    from_param: str = None,
    to: str = None,
    language: str = "en",
    sort_by: str = "relevancy",
    page: int = 1
):
    today = datetime.date.today()
    from_param = str(today - datetime.timedelta(days=7))
    to = str(today)
    return newsapi.get_everything(
        q=q,
        sources=sources,
        domains=domains,
        from_param=from_param,
        to=to,
        language=language,
        sort_by=sort_by,
        page=page
    )

# /v2/top-headlines/sources
async def fetch_sources(
    category: str = None,
    language: str = "en",
    country: str = "us"
):
    return newsapi.get_sources(
        category=category,
        language=language,
        country=country
    )

