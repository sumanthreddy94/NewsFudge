from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional

from typing import List

class QA(BaseModel):
    question: str
    answer: str
    created_at: datetime
    urls: Optional[List[str]] = []

class Conversation(BaseModel):
    id: str
    title: str
    qa_list: List[QA]
    created_at: datetime