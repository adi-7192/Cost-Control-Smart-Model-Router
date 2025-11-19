from typing import Dict, Type
from .base import BaseClassifier
from .rules import RuleBasedClassifier
from .llm import LLMClassifier

class ClassifierFactory:
    _registry: Dict[str, Type[BaseClassifier]] = {
        "rules": RuleBasedClassifier,
        "llm": LLMClassifier
    }

    @classmethod
    def register(cls, name: str, classifier_cls: Type[BaseClassifier]):
        """Register a new classifier class."""
        cls._registry[name] = classifier_cls

    @classmethod
    def get_classifier(cls, name: str) -> BaseClassifier:
        """Get a classifier instance by name."""
        classifier_cls = cls._registry.get(name)
        if not classifier_cls:
            raise ValueError(f"Classifier '{name}' not found. Available: {list(cls._registry.keys())}")
        return classifier_cls()
