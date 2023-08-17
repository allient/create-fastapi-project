from app.schemas.message_schema import (
    IChatResponse,
    IUserMessage,
)
from app.utils.adaptive_cards.cards import create_adaptive_card
from app.utils.callback import CustomAsyncCallbackHandler
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


@router.get("/chat")
async def home():
    return "Hello World"


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        user_message = data["message"]
        user_message_card = create_adaptive_card(user_message)

        resp = IChatResponse(
            sender="you",
            message=user_message_card.to_dict(),
            type="start",
            message_id=str(uuid7()),
            id=str(uuid7()),
        )
        await websocket.send_json(resp.dict())

        # message_id: str = str(uuid7())
        # start_resp = IChatResponse(
        #     sender="bot", message={}, type="start", message_id=message_id, id=""
        # )
        # await websocket.send_json(start_resp.dict())

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
        message_id: str = str(uuid7())
        custom_handler = CustomAsyncCallbackHandler(
            websocket=websocket, message_id=message_id
        )
        llm = ChatOpenAI(streaming=True, callbacks=[custom_handler])

        chat_llm_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory,
        )

        response = await chat_llm_chain.apredict(
            human_input=user_message,
        )
        print("#" * 100)
        print(response)
        print("#" * 100)
