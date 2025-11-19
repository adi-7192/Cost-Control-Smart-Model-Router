from typing import Dict, Type
from .base import LLMClient
from .providers import Phi3Client, Llama3Client, GPT4oClient

class LLMClientFactory:
    _registry: Dict[str, Type[LLMClient]] = {
        "phi3": Phi3Client,
        "llama3": Llama3Client,
        "gpt4o": GPT4oClient
    }

    @classmethod
    def register(cls, name: str, client_cls: Type[LLMClient]):
        """Register a new LLM client class."""
        cls._registry[name] = client_cls

    @classmethod
    def get_client(cls, name: str) -> LLMClient:
        """Get an LLM client instance by name."""
        client_cls = cls._registry.get(name)
        if not client_cls:
            raise ValueError(f"LLM Client '{name}' not found. Available: {list(cls._registry.keys())}")
        return client_cls()
