from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl
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
    url: HttpUrl
    site_full: str
    site: str
    site_section: Optional[HttpUrl]
    site_categories: List[str]
    section_title: Optional[str]
    title: str
    title_full: str
    published: datetime
    replies_count: int
    participants_count: int
    site_type: str
    country: str
    main_image: Optional[HttpUrl]
    performance_score: int
    domain_rank: int
    domain_rank_updated: datetime
    reach: Optional[int]
    social: SocialStats


class Entities(BaseModel):
    persons: List[str]
    organizations: List[str]
    locations: List[str]


class Article(BaseModel):
    thread: Thread
    uuid: str
    url: HttpUrl
    ord_in_thread: int
    parent_url: Optional[HttpUrl]
    author: Optional[str]
    published: datetime
    title: str
    text: str
    highlightText: Optional[str] = None
    highlightTitle: Optional[str] = None
    highlightThreadTitle: Optional[str] = None
    language: str
    sentiment: Optional[str] = None
    categories: List[str]
    webz_reporter: bool
    external_links: List[HttpUrl]
    external_images: List[HttpUrl]
    entities: Entities
    rating: Optional[float] = None
    crawled: datetime
    updated: datetime

# Cleaned Data
class ArticleMetadata(BaseModel):
    url: Optional[HttpUrl]
    author: Optional[str]
    published: Optional[str]
    site: Optional[str]

class CleanedArticle(BaseModel):
    id: str
    title: str
    text: str
    metadata: ArticleMetadata
