from pydantic import BaseModel
from typing import Any


class ICreateMediaAC(BaseModel):
    media_object: Any
    media_type: str
    url: str
