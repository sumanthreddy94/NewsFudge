from pydantic import BaseModel, HttpUrl
from typing import Optional

class SourceModel(BaseModel):
    id: Optional[str]
    name: str

class ArticleModel(BaseModel):
    source: SourceModel
    author: Optional[str]
    title: str
    description: Optional[str]
    url: HttpUrl
    urlToImage: Optional[HttpUrl]
    publishedAt: str
    content: Optional[str]

from typing import List

class NewsApiResponseModel(BaseModel):
    status: str
    totalResults: int
    articles: List[ArticleModel]