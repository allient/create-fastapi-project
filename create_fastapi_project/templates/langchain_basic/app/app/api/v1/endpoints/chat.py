from create_fastapi_project.templates.langchain_basic.app.app.main import app
from create_fastapi_project.templates.langchain_basic.app.app.schemas.message_schema import (
    IChatResponse,
    IUserMessage,
)
from fastapi import APIRouter, WebSocket
from app.utils.uuid6 import uuid7
from app.core.config import settings
from app.schemas.response_schema import IGetResponseBase, create_response

router = APIRouter()


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        message_data = IUserMessage.parse_obj(data)
        user_message = message_data.message

        resp = IChatResponse(
            sender="you",
            message=user_message.message,
            type="stream",
            message_id=str(uuid7()),
            id=str(uuid7()),
        )
        await websocket.send_json(resp.dict())

        start_resp = IChatResponse(
            sender="bot", message="", type="start", message_id="", id=""
        )
        await websocket.send_json(start_resp.dict())
