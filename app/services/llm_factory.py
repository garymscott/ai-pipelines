from typing import Any, Optional, Type
from pydantic import BaseModel
import instructor
from openai import OpenAI

class LLMConnector:
    def create_completion(
        self,
        messages: list[dict[str, str]],
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs: Any,
    ) -> Any:
        raise NotImplementedError

class OpenAIConnector(LLMConnector):
    def __init__(self):
        self.client = instructor.patch(OpenAI())

    def create_completion(
        self,
        messages: list[dict[str, str]],
        response_model: Optional[Type[BaseModel]] = None,
        **kwargs: Any,
    ) -> Any:
        if response_model:
            return self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                response_model=response_model,
                **kwargs,
            )
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content

class LLMFactory:
    _connectors = {
        "openai": OpenAIConnector,
    }

    @classmethod
    def register_connector(cls, name: str, connector: Type[LLMConnector]):
        cls._connectors[name] = connector

    @classmethod
    def get_connector(cls, name: str) -> LLMConnector:
        connector_class = cls._connectors.get(name)
        if not connector_class:
            raise ValueError(f"Unknown LLM connector: {name}")
        return connector_class()