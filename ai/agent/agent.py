from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    student: str
    ai: str

class AiReviewProblem(BaseModel):
    """the response text which is returned by llm"""
    no: str | None
    ans_student: str | None
    ans_ai: str | None
    conclusion: int | None
    reason: str  | None
    solution: str | None
    knowledge: str | None
    suggestion: str | None

class AiReviewInfo(BaseModel):
    summary: str
    problems: List[AiReviewProblem]
    total: int
    correct: int
    incorrect: int
    uncertain: int
    subject: str | None

class GoogleRestaurant(BaseModel):
    """Data model for a Google Restaurant."""

    restaurant: str
    food: str
    location: str
    category: str
    hours: str
    price: str
    rating: float
    review: str
    description: str
    nearby_tourist_places: str


class HandwritingText(BaseModel):
    text: str 