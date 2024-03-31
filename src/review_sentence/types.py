from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReviewRequest(BaseModel):
    word: str
    sense: str
    sentence: str


class ReviewResponse(BaseModel):
    score: int
    feedback: Optional[str] = None
    explanation: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
