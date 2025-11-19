from abc import ABC, abstractmethod

class BaseClassifier(ABC):
    @abstractmethod
    def classify(self, prompt: str) -> tuple[str, str]:
        """
        Classifies the prompt difficulty.
        Returns: (difficulty, reasoning)
        """
        pass
