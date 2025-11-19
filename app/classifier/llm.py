from .base import BaseClassifier
from ..config import settings
import asyncio
import os
import requests
import json

class LLMClassifier(BaseClassifier):
    def __init__(self):
        # Read from settings which loads from .env
        self.openai_key = settings.OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")
        self.google_key = settings.GOOGLE_API_KEY or os.environ.get("GOOGLE_API_KEY")

    async def classify_async(self, prompt: str) -> tuple[str, str]:
        # Try to use real LLM for classification
        if self.google_key:
            return await self._classify_with_gemini(prompt)
        elif self.openai_key and self.openai_key.startswith("sk-"):
            return await self._classify_with_openai(prompt)
        else:
            # Fallback to simple rules
            return self._fallback_classify(prompt)
    
    async def _classify_with_gemini(self, prompt: str) -> tuple[str, str]:
        """Use Gemini to intelligently classify prompt difficulty"""
        try:
            from ..llm.model_discovery import ModelDiscovery
            model = ModelDiscovery.get_cached_or_discover_gemini(self.google_key)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.google_key}"
            
            classification_prompt = f"""Analyze this user prompt and classify its complexity for LLM routing.

User Prompt: "{prompt}"

Classification Rules:
- SIMPLE: Basic facts, math, definitions, greetings (route to small model)
- MODERATE: Code tasks, explanations, how-to questions (route to medium model)  
- COMPLEX: Deep analysis, creative writing, multi-step reasoning (route to large model)

Respond ONLY with valid JSON in this exact format:
{{"difficulty": "simple|moderate|complex", "reasoning": "brief explanation"}}"""

            data = {
                "contents": [{"parts": [{"text": classification_prompt}]}],
                "generationConfig": {"temperature": 0.1}
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(url, headers={"Content-Type": "application/json"}, json=data)
            )
            
            if response.status_code == 200:
                res_json = response.json()
                text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                
                # Parse JSON response
                # Clean markdown code blocks if present
                text = text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0]
                
                result = json.loads(text.strip())
                difficulty = result.get("difficulty", "moderate").lower()
                reasoning = result.get("reasoning", "LLM classification")
                
                # Validate difficulty
                if difficulty not in ["simple", "moderate", "complex"]:
                    difficulty = "moderate"
                
                return difficulty, f"[Gemini Classifier] {reasoning}"
            else:
                return self._fallback_classify(prompt)
                
        except Exception as e:
            print(f"Gemini classification error: {e}")
            return self._fallback_classify(prompt)
    
    async def _classify_with_openai(self, prompt: str) -> tuple[str, str]:
        """Use OpenAI to intelligently classify prompt difficulty"""
        try:
            classification_prompt = f"""Analyze this user prompt and classify its complexity for LLM routing.

User Prompt: "{prompt}"

Classification Rules:
- SIMPLE: Basic facts, math, definitions, greetings (route to small model)
- MODERATE: Code tasks, explanations, how-to questions (route to medium model)  
- COMPLEX: Deep analysis, creative writing, multi-step reasoning (route to large model)

Respond ONLY with valid JSON in this exact format:
{{"difficulty": "simple|moderate|complex", "reasoning": "brief explanation"}}"""

            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": classification_prompt}],
                "temperature": 0.1,
                "max_tokens": 100
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            )
            
            if response.status_code == 200:
                res_json = response.json()
                text = res_json["choices"][0]["message"]["content"]
                
                # Parse JSON response
                text = text.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0]
                
                result = json.loads(text.strip())
                difficulty = result.get("difficulty", "moderate").lower()
                reasoning = result.get("reasoning", "LLM classification")
                
                # Validate difficulty
                if difficulty not in ["simple", "moderate", "complex"]:
                    difficulty = "moderate"
                
                return difficulty, f"[OpenAI Classifier] {reasoning}"
            else:
                return self._fallback_classify(prompt)
                
        except Exception as e:
            print(f"OpenAI classification error: {e}")
            return self._fallback_classify(prompt)
    
    def _fallback_classify(self, prompt: str) -> tuple[str, str]:
        """Simple rule-based fallback when no API keys available"""
        prompt_lower = prompt.lower()
        
        # Length-based
        if len(prompt) > 500:
            return "complex", "Long prompt (>500 chars)"
        
        # Keyword-based
        complex_keywords = ["explain", "analyze", "compare", "evaluate", "discuss", "philosophy", "theory"]
        moderate_keywords = ["write", "create", "function", "code", "how", "why", "python", "javascript"]
        
        for kw in complex_keywords:
            if kw in prompt_lower:
                return "complex", f"Contains complex keyword: '{kw}'"
        
        for kw in moderate_keywords:
            if kw in prompt_lower:
                return "moderate", f"Contains moderate keyword: '{kw}'"
        
        return "simple", "Short prompt with no complex keywords"

    def classify(self, prompt: str) -> tuple[str, str]:
        """Sync wrapper"""
        return asyncio.run(self.classify_async(prompt))
