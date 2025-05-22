import math
import datetime
from app.api.services.news_fetcher import fetch_everything
from app.models.news import NewsApiResponseModel
# from app.api.services.embedding import embed_and_store_articles

async def fetch_and_store_last_30_days(query: str = None, sources = "CNN,CNBC,al-jazeera-english,New York Post,Bloomberg"):
    today = datetime.date.today()
    from_date = (today - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    all_articles = []

    # First page fetch
    try:
        print(f"Fetching page 1 for {from_date} to {to_date}")
        response = await fetch_everything(
            q=query,
            sources=sources,
            from_param=from_date,
            to=to_date,
            page=1
        )
        newsResponse = NewsApiResponseModel(**response)
        total_results = newsResponse.totalResults
        
        articles = newsResponse.articles
        all_articles.extend(articles)

        total_pages = math.ceil(total_results / 100)
        print(f"Total articles: {total_results}, total pages: {total_pages}")

    except Exception as e:
        print(f"Error fetching page 1: {e}")
        return

    # Fetch remaining pages
    for page in range(2, total_pages + 1):
        try:
            print(f"Fetching page {page}")
            response = await fetch_everything(
                q=query,
                from_param=from_date,
                to=to_date,
                page=page,
                sources=sources
            )
            articles = NewsApiResponseModel(**response).articles
            if not articles:
                break
            all_articles.extend(articles)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

    print(f"Total articles fetched: {len(all_articles)}")
    if all_articles:
        ...
        # await embed_and_store_articles(all_articles)
