from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime


class SocialPlatformStats(BaseModel):
    likes: Optional[int] = 0
    comments: Optional[int] = 0
    shares: Optional[int] = 0


class SocialStats(BaseModel):
    facebook: Optional[SocialPlatformStats] = SocialPlatformStats()
    gplus: Optional[SocialPlatformStats] = SocialPlatformStats()
    pinterest: Optional[SocialPlatformStats] = SocialPlatformStats()
    linkedin: Optional[SocialPlatformStats] = SocialPlatformStats()
    stumbledupon: Optional[SocialPlatformStats] = SocialPlatformStats()
    vk: Optional[SocialPlatformStats] = SocialPlatformStats()


class Thread(BaseModel):
    uuid: str
    url: Optional[str] = None
    site_full: str
    site: str
    site_section: Optional[str] = None
    site_categories: List[str]
    section_title: Optional[str] = None
    title: str
    title_full: str
    published: datetime
    replies_count: int
    participants_count: int
    site_type: str
    country: Optional[str]
    main_image: Optional[str] = None
    performance_score: int
    domain_rank: int
    domain_rank_updated: datetime
    reach: Optional[int] = None
    social: SocialStats


class EntityItem(BaseModel):
    name: str
    sentiment: Optional[str] = None

class Entities(BaseModel):
    persons: Optional[List[EntityItem]] = []
    organizations: Optional[List[EntityItem]] = []
    locations: Optional[List[EntityItem]] = []


class Article(BaseModel):
    thread: Thread
    uuid: str
    url: Optional[str] = None
    ord_in_thread: int
    parent_url: Optional[str] = None
    author: Optional[str] = None
    published: str
    title: str
    text: str
    highlightText: Optional[str] = None
    highlightTitle: Optional[str] = None
    highlightThreadTitle: Optional[str] = None
    language: str
    sentiment: Optional[str] = None
    categories: Optional[List[str]] = None
    webz_reporter: Optional[bool] = None
    external_links: Optional[List[str]] = None
    external_images: Optional[List[str]] = None
    entities: Entities
    rating: Optional[float] = None
    crawled: str
    updated: str

# Cleaned Data
class ArticleMetadata(BaseModel):
    url: Optional[str] = None
    author: Optional[str] = None
    published: Optional[str] = None
    site: Optional[str] = None

class CleanedArticle(BaseModel):
    id: str
    title: str
    text: str
    metadata: ArticleMetadata

# Retriever Ranked Result (RAW)
class SearchResultItem(BaseModel):
    text_snippet: str
    title: Optional[str] = None
    url: Optional[str] = None
