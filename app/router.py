from sqlalchemy.orm import Session
import os
from .classifier.base import BaseClassifier
from .classifier.rules import RuleBasedClassifier
from .classifier.llm import LLMClassifier
from .llm.base import LLMClient
from .llm.providers import Phi3Client, GPT4oClient, GeminiClient
from .config import settings
from .models import RouteResponse, RequestLog
import time

class ModelRouter:
    def __init__(self):
        # Auto-detect: Use LLM classifier if API keys are available for smarter routing
        has_api_keys = settings.OPENAI_API_KEY or settings.GOOGLE_API_KEY
        
        if settings.CLASSIFIER_TYPE == "llm" or has_api_keys:
            self.classifier = LLMClassifier()
            print(f"Using LLM-based classifier for intelligent routing (OpenAI: {bool(settings.OPENAI_API_KEY)}, Google: {bool(settings.GOOGLE_API_KEY)})")
        else:
            self.classifier = RuleBasedClassifier()
            print("Using rule-based classifier")
            
        self.clients = {
            "simple": Phi3Client(),
            "moderate": GeminiClient(), # Use Gemini (falls back to Llama sim)
            "complex": GPT4oClient()
        }
        
        self.model_names = {
            "simple": "Phi-3-Mini",
            "moderate": "Gemini 2.5 Flash",
            "complex": "GPT-4o"
        }

    async def route_and_execute(self, prompt: str, db: Session) -> RouteResponse:
        start_time = time.time()
        
        # 1. Classify
        if isinstance(self.classifier, LLMClassifier):
            difficulty, reasoning = await self.classifier.classify_async(prompt)
        else:
            difficulty, reasoning = self.classifier.classify(prompt)
        
        # 2. Select Client
        client = self.clients.get(difficulty, self.clients["complex"])
        model_name = self.model_names.get(difficulty, "GPT-4o")
        
        # 3. Execute
        response_text, cost, tokens = await client.generate(prompt)
        
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        
        # 4. Log
        log_entry = RequestLog(
            prompt_preview=prompt[:50],
            difficulty=difficulty,
            reasoning=reasoning,
            model_used=model_name,
            cost=cost,
            tokens_used=tokens,
            response_time_ms=latency
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        
        return RouteResponse(
            model=model_name,
            difficulty=difficulty,
            reasoning=reasoning,
            response=response_text,
            cost=cost,
            tokens=tokens,
            latency_ms=latency
        )
