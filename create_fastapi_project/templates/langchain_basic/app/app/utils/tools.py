from typing import Any, Optional
from langchain.tools import BaseTool
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import httpx

pokemon_api_url = "https://pokeapi.co/api/v2/pokemon/"


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


class PokemonSearchTool(BaseTool):
    name = "search_pokemon"
    description = " Useful when asked to answer information about a pokemon"
    # return_direct = True

    def __init__(self):
        super().__init__()
        # self.return_direct = True

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool."""
        response = httpx.get(pokemon_api_url + query)
        body = response.json()
        data = body.get("data", {})
        affirmation = data.get("text", "Hoy va a ser un gran día")
        return affirmation

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        """Use the tool asynchronously."""
        # create a async client with httpx and get request
        async with httpx.AsyncClient() as client:
            pokemon_url = pokemon_api_url + query.lower()
            print("#" * 100)
            print(pokemon_url)
            print("#" * 100)
            response = await client.get(pokemon_url)
            body = response.json()
            pokemon_number = body.get("id", 1)
            pokemon_name = body.get("name", "pikachu")
            pokemon_image = body.get("sprites", {}).get(
                "front_default",
                "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
            )
            pokemon_types = body.get("types", [])
            pokemon_type = pokemon_types[0].get("type", {}).get("name", "electric")
            abilities = body.get("abilities", [])
            abilities_list_names = []
            height = body["height"] / 10  # convert to meters
            weight = body["weight"] / 10  # convert to kg
            for ability in abilities:
                abilities_list_names.append(ability["ability"]["name"])
            abilities_names = ", ".join(abilities_list_names)
            # create a card with the information
            return f"""{pokemon_image} \n
{pokemon_name} - #{pokemon_number} \n
Abilities: {abilities_names} \n
Type: {pokemon_type} \n
Height: {height} m \n
Weight: {weight} kg \n
Sprite: {pokemon_image} \n
"""
            return pokemon_image
            return {
                "pokemon_number": pokemon_number,
                "pokemon_name": pokemon_name,
                "pokemon_image": pokemon_image,
                "pokemon_type": pokemon_type,
                "abilities": abilities,
            }
