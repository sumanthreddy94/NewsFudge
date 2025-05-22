import httpx

from app.core.config import NEWS_API_URL, NEWS_API_KEY

async def get_sources():
    if not NEWS_API_KEY:
        return {"error": "Missing NEWS_API_KEY in environment."}
    
    headers = {
        "X-Api-Key": NEWS_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NEWS_API_URL+ '/top-headlines/sources', headers= headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as err:
            return {"error": str(err)}