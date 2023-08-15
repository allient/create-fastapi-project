from app.schemas.message_schema import (
    IChatResponse,
    IUserMessage,
)
from fastapi import APIRouter, WebSocket
from app.utils.uuid6 import uuid7
from app.core.config import settings
from app.schemas.response_schema import IGetResponseBase, create_response

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain


router = APIRouter()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        user_message = data["message"]

        resp = IChatResponse(
            sender="you",
            message=user_message,
            type="stream",
            message_id=str(uuid7()),
            id=str(uuid7()),
        )
        await websocket.send_json(resp.dict())

        start_resp = IChatResponse(
            sender="bot", message="", type="start", message_id="", id=""
        )
        await websocket.send_json(start_resp.dict())

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content="You are a chatbot having a conversation with a human."
                ),  # The persistent system prompt
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # Where the memory will be stored.
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # Where the human input will injectd
            ]
        )

        llm = ChatOpenAI()

        chat_llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory,
            callbacks=[],
        )

        response = chat_llm_chain.predict(human_input=user_message)
        print("#" * 100)
        print(response)
        print("#" * 100)
