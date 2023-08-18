
from typing import Any, Optional
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from app.core.config import settings
import httpx
class GeneralKnowledgeTool(BaseTool):
    name = "Search"
    description = (
        # "Useful when needs to recommend general knowledge and mantains a conversation"
        # "Useful when needs general answers and mantains a conversation"
        "useful for when you need to answer questions about current events"
    )

    def __init__(self):
        super().__init__()
        # self.return_direct = True

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        # create a async client with httpx and get request
        chat = ChatOpenAI()
        response = await chat.agenerate([[HumanMessage(content=query)]])
        message = response.generations[0][0].text
        return message



class GeneralWeatherTool(BaseTool):
    name = "Weather"
    description = "useful for when you need to answer questions about weather"

    def __init__(self):
        super().__init__()
        # self.return_direct = True

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass
    
    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> dict:
        """Use the tool asynchronously."""
        async with httpx.AsyncClient() as client:
            print("query", query )
            response = await client.get(f"{settings.WHEATER_URL}/{query}?format=j1")
            weather = response.json()
            temperature = weather["current_condition"][0]
            return temperature