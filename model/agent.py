from pydantic import BaseModel
from typing import List
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime

import json
from typing import Protocol
from dataclasses import dataclass
from dataclass_wizard import JSONWizard


class Answer(BaseModel):
    student: str
    ai: str

class Assignment(BaseModel):
    """the response text which is returned by llm"""
    no: str | None
    ans_student: str | None
    ans_ai: str | None
    conclusion: int | None
    reason: str  | None
    solution: str | None
    knowledge: str | None
    suggestions: str | None

class ReviewInfo(BaseModel):
    summary: str
    problems: List[Assignment]
    total: int
    correct: int
    incorrect: int
    uncertain: int

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