from app.core.config import settings
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.tools import BaseTool
from serpapi import GoogleSearch
from typing import Any, Optional
import httpx

pokemon_api_url = "https://pokeapi.co/api/v2/pokemon/"
unsplash_api_url = f"https://api.unsplash.com/search/photos?client_id={settings.UNSPLASH_API_KEY}&query="
weather_api_url = "https://wttr.in"


class GeneralKnowledgeTool(BaseTool):
    name = "Search"
    description = "useful for when you need to answer questions about current events"

    def __init__(self):
        super().__init__()

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        chat = ChatOpenAI()
        response = await chat.agenerate([[HumanMessage(content=query)]])
        message = response.generations[0][0].text
        return message


class PokemonSearchTool(BaseTool):
    name = "search_pokemon"
    description = " Useful when asked to answer information about a pokemon"

    def __init__(self):
        super().__init__()

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        response = httpx.get(pokemon_api_url + query)
        body = response.json()
        pokemon_number = body["id"]
        pokemon_name = body["name"]
        return f"{pokemon_name} - #{pokemon_number} "

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        async with httpx.AsyncClient() as client:
            pokemon_url = pokemon_api_url + query.lower()
            response = await client.get(pokemon_url)
            if response.status_code == 404:
                return "Pokemon not found"
            body = response.json()
            pokemon_number = body["id"]
            pokemon_name = body["name"]
            pokemon_image = body.get("sprites", {}).get(
                "front_default",
                "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
            )
            pokemon_types = body["types"]
            pokemon_type = pokemon_types[0].get("type", {}).get("name", "electric")
            abilities = body.get("abilities", [])
            abilities_list_names = []
            height = body["height"] / 10  # convert to meters
            weight = body["weight"] / 10  # convert to kg
            for ability in abilities:
                abilities_list_names.append(ability["ability"]["name"])
            abilities_names = ", ".join(abilities_list_names)
            return f"""{pokemon_image} \n
{pokemon_name} - #{pokemon_number} \n
Abilities: {abilities_names} \n
Type: {pokemon_type} \n
Height: {height} m \n
Weight: {weight} kg \n
Sprite: {pokemon_image} \n
"""


class ImageSearchTool(BaseTool):
    name = "search_image"
    description = " Useful when asked to answer information about find images URL"
    return_direct = True

    def __init__(self):
        super().__init__()

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        async with httpx.AsyncClient() as client:
            if settings.UNSPLASH_API_KEY == "":
                return "You need to set a UNSPLASH_API_KEY"

            unsplash_url = unsplash_api_url + query.lower()
            response = await client.get(unsplash_url)
            body = response.json()
            results = body["results"]
            images_urls = []
            for result in results:
                image_url = result["urls"]["small"]
                images_urls.append(image_url)
            image_list_string = "\n".join(
                [f"{i+1}. ![Image {i+1}]({url})" for i, url in enumerate(images_urls)]
            )
            return image_list_string


class YoutubeSearchTool(BaseTool):
    name = "search_videos"
    description = " Useful when asked to answer information about find videos"
    return_direct = True

    def __init__(self):
        super().__init__()

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        pass

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        async with httpx.AsyncClient() as client:
            if not settings.SERP_API_KEY or settings.SERP_API_KEY == "":
                return "You need to set a SERP_API_KEY"

            params = {
                "engine": "youtube",
                "search_query": query,
                "api_key": settings.SERP_API_KEY,
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            videos = results["video_results"]
            video_list_string = "\n".join(
                [
                    f"{i+1}. [{video['title']}]({video['link']})"
                    for i, video in enumerate(videos)
                ]
            )
            return video_list_string


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
            query = query.replace(" ", "+")
            query = query.replace(",", "")
            final_url = f"{weather_api_url}/{query}?format=j1"
            response = await client.get(final_url)
            if response.status_code == 404:
                return f"Could not find weather for {query}"
            weather = response.json()
            temperature = weather["current_condition"][0]
            return temperature
