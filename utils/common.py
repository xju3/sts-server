import base64
from pydantic import BaseModel
from PIL import Image
import matplotlib.pyplot as plt

import json
from typing import Protocol



class JsonSerializable(Protocol):
    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def __repr__(self) -> str:
        return self.to_json()
    
def encode_image(image_path):
    """Convert image to base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")