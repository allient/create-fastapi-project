from pydantic import BaseModel, field_validator
from app.utils.uuid6 import uuid7
from typing import Any


class IUserMessage(BaseModel):
    """User message schema."""

    message: str


class IChatResponse(BaseModel):
    """Chat response schema."""

    id: str
    message_id: str
    sender: str
    message: Any
    type: str
    suggested_responses: list[str] = []

    @field_validator("id", "message_id")
    def check_ids(cls, v):
        if v == "" or v is None:
            return str(uuid7())
        return v

    @field_validator("sender")
    def sender_must_be_bot_or_you(cls, v):
        if v not in ["bot", "you"]:
            raise ValueError("sender must be bot or you")
        return v

    @field_validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v