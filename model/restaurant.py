from pydantic import BaseModel
from PIL import Image
import matplotlib.pyplot as plt

import json
from typing import Protocol
from dataclasses import dataclass

from dataclass_wizard import JSONWizard

class JsonSerializable(Protocol):
    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def __repr__(self) -> str:
        return self.to_json()

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


@dataclass
class Ticket(JSONWizard):
    """ticket id after uploading image successfully."""
    ticketId: str
    
    def __init__(self, _ticket_id: str = None):
        self.ticketId = _ticket_id

@dataclass
class ErrMsg(JSONWizard): 
    """error message."""
    code: str
    msg: str
    def __init__(self, _code: str = None, _msg : str = None) -> None:
        self.code = _code
        self.msg = _msg

@dataclass
class HttpResult(JSONWizard):
    """this data is used for http response."""
    err: ErrMsg
    data: any

    def __init__(self, _err : ErrMsg = None, _data : any = None) -> None:
        self.err = _err
        self.data = _data



