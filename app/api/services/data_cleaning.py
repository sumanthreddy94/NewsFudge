import re
import uuid
from typing import List, Tuple

from app.core.config import COLLECTION_NAME
from app.db.db_client import get_persist_chroma
from app.models.news_dataset import Article, ArticleMetadata, CleanedArticle
from app.tasks.data_ingest import load_articles_from_directory


def clean_text(text):
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # Remove markdown-style links
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    
    # Remove boilerplate junk phrases
    junk_phrases = ['Publicidad', 'Compartir', 'Comentar es una ventaja', 'Necesitas ser registrado']
    for phrase in junk_phrases:
        text = text.replace(phrase, '')
    
    # Lowercase and trim whitespace
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    
    return text


def process_json_file(article: Article) -> CleanedArticle | None:
    if article.language.lower() != "english":
        return None  # Skip non-English

    cleaned_text = clean_text(article.text)
    if len(cleaned_text.split()) < 50:
        return None  # Skip very short entries

    return CleanedArticle(
        id=article.uuid,
        title=clean_text(article.title),
        text=cleaned_text,
        metadata=ArticleMetadata(
            url=article.url,
            author=article.author,
            published=article.published,
            site=article.thread.site
        )
    )


def load_and_clean_all() -> List[CleanedArticle]:
    cleaned_data = []
    chroma = get_persist_chroma()
    collections = chroma.list_collections()
    if COLLECTION_NAME in collections:
        return cleaned_data
    articles = load_articles_from_directory()
    for article in articles:
        cleaned = process_json_file(article)
        cleaned_data.append(cleaned)
    return cleaned_data


def sanitize_metadata(metadata: ArticleMetadata) -> dict:
    return {
        "title": getattr(metadata, "title", "") or "",
        "url": metadata.url or "",
        "author": metadata.author or "",
        "published": metadata.published or "",
        "site": metadata.site or "",
    }


def prepare_documents_for_embedding(
    articles: List[CleanedArticle]
) -> Tuple[List[str], List[dict], List[str]]:
    documents = []
    metadatas = []
    ids = []
    seen_ids = set()

    for article in articles:
        if article is None:
            continue

        # Compose combined text safely, skip if empty
        doc_text = f"{article.title or ''}. {article.text or ''}".strip()
        if not doc_text:
            continue
        
        documents.append(doc_text)

        # Deduplicate IDs
        current_id = article.id
        if current_id in seen_ids:
            current_id = str(uuid.uuid4())
        seen_ids.add(current_id)
        ids.append(current_id)

        # Sanitize metadata safely, fallback to empty ArticleMetadata if None
        metadatas.append(
            sanitize_metadata(article.metadata or ArticleMetadata())
        )

    return documents, metadatas, ids