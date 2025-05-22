import os
import json
from typing import List
from pathlib import Path
from app.models.news_dataset import Article
from app.core.config import DATASET_PATH

def load_articles_from_directory() -> List[Article]:
    articles = []
    for root, _, files in os.walk(DATASET_PATH):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        article = Article(**data)
                        articles.append(article)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
    return articles
