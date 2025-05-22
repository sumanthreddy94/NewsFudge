import os
import json
import re

from fastapi.background import P

from app.models.news_dataset import Article, ArticleMetadata, CleanedArticle

from app.tasks.data_ingest import load_articles_from_directory

def clean_text(text):
    if not text:
        return ""
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # Remove markdown-style links
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    
    # Remove boilerplate
    junk_phrases = ['Publicidad', 'Compartir', 'Comentar es una ventaja', 'Necesitas ser registrado']
    for phrase in junk_phrases:
        text = text.replace(phrase, '')
    
    # Lowercase and trim
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    
    return text

def process_json_file(article: Article):
    
    if article.language.lower() != "english":
        return None  # Skip non-English

    cleaned_text = clean_text(article.text)
    if len(cleaned_text.split()) < 50:
        return None  # Skip very short entries

    return CleanedArticle(
        id = article.uuid,
        title=clean_text(article.title),
        text=cleaned_text,
        metadata = ArticleMetadata(
            url=article.url,
            author=article.author,
            published=article.published,
            site=article.thread.site
        )
    )

def load_and_clean_all():
    cleaned_data = []
    articles = load_articles_from_directory()
    for article in articles:
        cleaned = process_json_file(article)
        cleaned_data.append(cleaned)
    return cleaned_data
