from app.core.config import settings
from app.schemas.message_schema import (
    IChatResponse,
)
import logging
from app.utils.adaptive_cards.cards import create_adaptive_card
from app.utils.callback import (
    CustomAsyncCallbackHandler,
    CustomFinalStreamingStdOutCallbackHandler,
)
from app.utils.tools import (
    GeneralKnowledgeTool,
    ImageSearchTool,
    PokemonSearchTool,
    YoutubeSearchTool,
    GeneralWeatherTool,
)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.uuid6 import uuid7
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.agents import ZeroShotAgent, AgentExecutor
from app.utils.prompt_zero import zero_agent_prompt

router = APIRouter()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    if not settings.OPENAI_API_KEY.startswith("sk-"):
        await websocket.send_json({"error": "OPENAI_API_KEY is not set"})
        return

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
            verbose=False,
            memory=memory,
        )

        await chat_llm_chain.apredict(
            human_input=user_message,
        )


@router.websocket("/tools")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    if not settings.OPENAI_API_KEY.startswith("sk-"):
        await websocket.send_json({"error": "OPENAI_API_KEY is not set"})
        return

    while True:
        try:
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
            message_id: str = str(uuid7())
            custom_handler = CustomFinalStreamingStdOutCallbackHandler(
                websocket, message_id=message_id
            )

            tools = [
                GeneralKnowledgeTool(),
                PokemonSearchTool(),
                ImageSearchTool(),
                YoutubeSearchTool(),
                GeneralWeatherTool(),
            ]

            llm = ChatOpenAI(
                streaming=True,
                temperature=0,
            )

            agent = ZeroShotAgent.from_llm_and_tools(
                llm=llm,
                tools=tools,
                prefix=zero_agent_prompt.prefix,
                suffix=zero_agent_prompt.suffix,
                format_instructions=zero_agent_prompt.format_instructions,
                input_variables=zero_agent_prompt.input_variables,
            )
            # TODO: We should use this
            # * max_execution_time=1,
            # early_stopping_method="generate",
            agent_executor = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=tools,
                verbose=False,
                handle_parsing_errors=True,
                memory=memory,
            )

            await agent_executor.arun(input=user_message, callbacks=[custom_handler])
        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
