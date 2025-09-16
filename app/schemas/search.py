from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Any

class SearchResponse(BaseModel):
    searchQuestion: str
    answer: Any  # JSON/dict
    # userEmail: EmailStr
    # userLocation: Optional[str]
    # userNationality: Optional[str]
    # createdAt: datetime
    # threadId: Optional[str]
