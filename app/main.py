from fastapi import FastAPI
from app.api.services.conversations_service import add_conversation, get_all_conversations, get_conversation_by_id, update_conversation
from app.api.services.data_cleaning import load_and_clean_all
from app.api.services.embeddings import embed_articles
from app.api.services.news_fetcher import fetch_top_headlines, fetch_everything, fetch_sources
from app.api.services.query import get_by_query, search_chroma
from app.models.conversations import QA, Conversation
from app.tasks.daily_fetch import fetch_and_store_last_30_days
from app.tasks.data_ingest import load_articles_from_directory

app = FastAPI(
    title="NewsFudge",
    version="0.1.0",
    description="Fast API AI APP"
)

@app.get("/")
def root():
    return {"message":"Welcome to News Fudge"}

@app.get("/sources")
async def get_news_sources(category: str = None, language: str = "en", country: str = "us"):
    return fetch_sources(category=category, language=language, country=country)

@app.get("/headlines")
async def get_headlines(
    q: str = None,
    sources: str = None,
    category: str = None,
    language: str = "en",
    country: str = "us"
):
    return await fetch_top_headlines(q=q, sources=sources, category=category, language=language, country=country)

@app.get("/everything")
async def get_all_articles(
    q: str,
    sources: str = None,
    domains: str = None,
    from_param: str = None,
    to: str = None,
    language: str = "en",
    sort_by: str = "relevancy",
    page: int = 1
):
    return await fetch_everything(
        q=q,
        sources=sources,
        domains=domains,
        from_param=from_param,
        to=to,
        language=language,
        sort_by=sort_by,
        page=page
    )

@app.get("/query")
async def query(query: str):
    return await get_by_query(query=query)

@app.post(path="/conversations")
async def create_conversation(conversation: Conversation):
    await add_conversation(conversation=conversation)

@app.get(path="/conversations")
async def get_conversations():
    conversations = await get_all_conversations()
    return conversations

@app.get(path="/conversations/{conv_id}")
async def get_conversations(conv_id: str):
    conversations = await get_conversation_by_id(convo_id=conv_id)
    return conversations

@app.post(path="/question/{conv_id}")
async def add_question(conv_id:str, qa: QA):
    await update_conversation(conv_id, qa)


@app.on_event(event_type="startup")
def startup_event():
    print("Starting Data Ingestion...")
    cleaned_articles = load_and_clean_all()
    if len(cleaned_articles) == 0:
        return
    embed_articles(cleaned_articles)





