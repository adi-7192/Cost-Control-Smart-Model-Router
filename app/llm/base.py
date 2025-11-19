from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 100) -> tuple[str, float, int]:
        """
        Generates text from the model.
        Returns: (response_text, cost_usd, tokens_used)
        """
        pass
