from app.schemas.message_schema import IChatResponse
from app.utils.adaptive_cards.cards import create_adaptive_card, create_image_card
from app.utils.chains import get_suggestions_questions
from langchain.callbacks.base import AsyncCallbackHandler
from app.utils.uuid6 import uuid7
from fastapi import WebSocket
from uuid import UUID
from typing import Any
from langchain.schema.agent import AgentFinish
from langchain.schema.output import LLMResult


DEFAULT_ANSWER_PREFIX_TOKENS = ["Final", " Answer", ":"]


class CustomAsyncCallbackHandler(AsyncCallbackHandler):
    def append_to_last_tokens(self, token: str) -> None:
        self.last_tokens.append(token)
        self.last_tokens_stripped.append(token.strip())
        if len(self.last_tokens) > len(self.answer_prefix_tokens):
            self.last_tokens.pop(0)
            self.last_tokens_stripped.pop(0)

    def check_if_answer_reached(self) -> bool:
        if self.strip_tokens:
            return self.last_tokens_stripped == self.answer_prefix_tokens_stripped
        else:
            return self.last_tokens == self.answer_prefix_tokens

    def update_message_id(self, message_id: str = str(uuid7())):
        self.message_id = message_id

    def __init__(
        self,
        websocket: WebSocket,
        *,
        message_id: str = str(uuid7()),
        answer_prefix_tokens: list[str] | None = None,
        strip_tokens: bool = True,
        stream_prefix: bool = False,
    ) -> None:
        """Instantiate FinalStreamingStdOutCallbackHandler.

        Args:
            answer_prefix_tokens: Token sequence that prefixes the answer.
                Default is ["Final", "Answer", ":"]
            strip_tokens: Ignore white spaces and new lines when comparing
                answer_prefix_tokens to last tokens? (to determine if answer has been
                reached)
            stream_prefix: Should answer prefix itself also be streamed?
        """
        self.websocket: WebSocket = websocket
        self.message_id: str = message_id
        self.text: str = ""
        self.started: bool = False
        self.loading_card = create_image_card(
            "https://res.cloudinary.com/dnv0qwkrk/image/upload/v1691005682/Alita/Ellipsis-2.4s-81px_1_nja8hq.gif"
        )
        self.adaptive_card = self.loading_card

        if answer_prefix_tokens is None:
            self.answer_prefix_tokens = DEFAULT_ANSWER_PREFIX_TOKENS
        else:
            self.answer_prefix_tokens = answer_prefix_tokens
        if strip_tokens:
            self.answer_prefix_tokens_stripped = [
                token.strip() for token in self.answer_prefix_tokens
            ]
        else:
            self.answer_prefix_tokens_stripped = self.answer_prefix_tokens
        self.last_tokens = [""] * len(self.answer_prefix_tokens)
        self.last_tokens_stripped = [""] * len(self.answer_prefix_tokens)
        self.strip_tokens = strip_tokens
        self.stream_prefix = stream_prefix
        self.answer_reached = False

    async def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""

        resp = IChatResponse(
            id="",
            message_id=self.message_id,
            sender="bot",
            message=self.loading_card.to_dict(),
            type="start",
        )
        await self.websocket.send_json(resp.dict())

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        # Remember the last n tokens, where n = len(answer_prefix_tokens)
        self.append_to_last_tokens(token)

        self.text += f"{token}"
        self.adaptive_card = create_adaptive_card(self.text)
        resp = IChatResponse(
            # id=str(uuid7()),
            id="",
            message_id=self.message_id,
            sender="bot",
            message=self.adaptive_card.to_dict(),
            type="stream",
        )
        await self.websocket.send_json(resp.dict())

    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM ends running."""
        resp = IChatResponse(
            id="",
            message_id=self.message_id,
            sender="bot",
            message=self.adaptive_card.to_dict(),
            type="end",
        )
        await self.websocket.send_json(resp.dict())


class CustomFinalStreamingStdOutCallbackHandler(AsyncCallbackHandler):
    """Callback handler for streaming in agents.
    Only works with agents using LLMs that support streaming.

    Only the final output of the agent will be streamed.
    """

    def append_to_last_tokens(self, token: str) -> None:
        self.last_tokens.append(token)
        self.last_tokens_stripped.append(token.strip())
        if len(self.last_tokens) > len(self.answer_prefix_tokens):
            self.last_tokens.pop(0)
            self.last_tokens_stripped.pop(0)

    def check_if_answer_reached(self) -> bool:
        if self.strip_tokens:
            return self.last_tokens_stripped == self.answer_prefix_tokens_stripped
        else:
            return self.last_tokens == self.answer_prefix_tokens

    def update_message_id(self, message_id: str = str(uuid7())):
        self.message_id = message_id

    def __init__(
        self,
        websocket: WebSocket,
        *,
        message_id: str = str(uuid7()),
        answer_prefix_tokens: list[str] | None = None,
        strip_tokens: bool = True,
        stream_prefix: bool = False,
    ) -> None:
        """Instantiate FinalStreamingStdOutCallbackHandler.

        Args:
            answer_prefix_tokens: Token sequence that prefixes the answer.
                Default is ["Final", "Answer", ":"]
            strip_tokens: Ignore white spaces and new lines when comparing
                answer_prefix_tokens to last tokens? (to determine if answer has been
                reached)
            stream_prefix: Should answer prefix itself also be streamed?
        """
        self.websocket: WebSocket = websocket
        self.message_id: str = message_id
        self.text: str = ""
        self.started: bool = False
        self.loading_card = create_image_card(
            "https://res.cloudinary.com/dnv0qwkrk/image/upload/v1691005682/Alita/Ellipsis-2.4s-81px_1_nja8hq.gif"
        )
        self.adaptive_card = self.loading_card

        if answer_prefix_tokens is None:
            self.answer_prefix_tokens = DEFAULT_ANSWER_PREFIX_TOKENS
        else:
            self.answer_prefix_tokens = answer_prefix_tokens
        if strip_tokens:
            self.answer_prefix_tokens_stripped = [
                token.strip() for token in self.answer_prefix_tokens
            ]
        else:
            self.answer_prefix_tokens_stripped = self.answer_prefix_tokens
        self.last_tokens = [""] * len(self.answer_prefix_tokens)
        self.last_tokens_stripped = [""] * len(self.answer_prefix_tokens)
        self.strip_tokens = strip_tokens
        self.stream_prefix = stream_prefix
        self.answer_reached = False

    async def on_llm_start(
        self, serialized: dict[str, Any], prompts: list[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        if self.started == False:
            self.started = True
            resp = IChatResponse(
                id="",
                message_id=self.message_id,
                sender="bot",
                message=self.loading_card.to_dict(),
                type="start",
            )
            await self.websocket.send_json(resp.dict())

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        **kwargs: Any,
    ) -> Any:
        """Run on agent end."""
        message: str = (
            self.text
            if self.text != ""
            # else "😕 Lo siento no he podido hallar lo que buscabas"
            else finish.return_values["output"]
        )
        self.adaptive_card = create_adaptive_card(message)

        resp = IChatResponse(
            id="",
            message_id=self.message_id,
            sender="bot",
            message=self.adaptive_card.to_dict(),
            type="stream",
        )
        await self.websocket.send_json(resp.dict())

        suggested_responses = await get_suggestions_questions(message)
        if len(suggested_responses) > 0:
            self.adaptive_card = create_adaptive_card(
                answer=message,
            )
        medium_resp = IChatResponse(
            id="",
            message_id=self.message_id,
            sender="bot",
            message=self.adaptive_card.to_dict(),
            type="end",
            suggested_responses=suggested_responses,
        )
        await self.websocket.send_json(medium_resp.dict())

        # Reset values
        self.text = ""
        self.answer_reached = False
        self.started = False

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        # Remember the last n tokens, where n = len(answer_prefix_tokens)
        self.append_to_last_tokens(token)

        # Check if the last n tokens match the answer_prefix_tokens list ...
        if self.check_if_answer_reached():
            self.answer_reached = True
            return

        # ... if yes, then print tokens from now on
        if self.answer_reached:
            self.text += f"{token}"
            self.adaptive_card = create_adaptive_card(self.text)

            resp = IChatResponse(
                id="",
                message_id=self.message_id,
                sender="bot",
                message=self.adaptive_card.to_dict(),
                type="stream",
            )
            await self.websocket.send_json(resp.dict())
