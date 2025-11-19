import asyncio
import random
import os
import asyncio
import os
import requests
from .base import LLMClient

class Phi3Client(LLMClient):
    async def generate(self, prompt: str, max_tokens: int = 100) -> tuple[str, float, int]:
        await asyncio.sleep(0.1) # Simulate latency
        
        # Simple mock logic for demo
        if "2*2" in prompt or "2+2" in prompt:
            response = "The answer is 4."
        else:
            response = f"[Phi-3] Processed simple request: {prompt[:20]}..."
            
        return response, 0.000046, len(prompt.split()) + 20

class GeminiClient(LLMClient):
    def __init__(self):
        from .model_discovery import ModelDiscovery
        from ..config import settings
        
        # Read from settings (which loads from .env) or os.environ
        self.api_key = settings.GOOGLE_API_KEY or os.environ.get("GOOGLE_API_KEY")
        self.model = None
        
        # Auto-discover best available model
        if self.api_key:
            self.model = ModelDiscovery.get_cached_or_discover_gemini(self.api_key)
            print(f"✓ GeminiClient initialized with model: {self.model}")
    
    async def generate(self, prompt: str, max_tokens: int = 100) -> tuple[str, float, int]:
        api_key = self.api_key
        
        if api_key and self.model:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
                headers = {"Content-Type": "application/json"}
                data = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, 
                    lambda: requests.post(url, headers=headers, json=data)
                )
                
                if response.status_code == 200:
                    res_json = response.json()
                    try:
                        text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                        # Estimate tokens (Gemini doesn't always return usage in simple response, or structure varies)
                        # But usually it's in usageMetadata if requested. For now, simple estimate.
                        tokens = len(text.split()) * 1.3 
                        cost = (tokens / 1000) * 0.0005 # Flash is very cheap
                        return f"[Gemini 2.5 Flash] {text}", cost, int(tokens)
                    except (KeyError, IndexError):
                         return f"[Error] Gemini response parsing failed: {response.text}", 0.0, 0
                else:
                    return f"[Error] Gemini API failed: {response.text}", 0.0, 0
            except Exception as e:
                return f"[Error] Exception calling Gemini: {str(e)}", 0.0, 0

        # Fallback to Llama 3 Simulation
        await asyncio.sleep(0.3)
        response = f"[Llama-3 (Simulated)] Processed moderate request: {prompt[:20]}..."
        return response, 0.00029, len(prompt.split()) + 50

class Llama3Client(LLMClient):
    # Kept for backward compatibility or specific use
    async def generate(self, prompt: str, max_tokens: int = 100) -> tuple[str, float, int]:
        # Simulate medium latency and cost
        await asyncio.sleep(0.3)
        response = f"[Llama-3] Processed moderate request: {prompt[:20]}..."
        return response, 0.00029, len(prompt.split()) + 50

class GPT4oClient(LLMClient):
    async def generate(self, prompt: str, max_tokens: int = 100) -> tuple[str, float, int]:
        # Simulate high latency and high cost (or call actual API if key provided)
        # For this demo, we simulate.
        await asyncio.sleep(0.8)
        tokens = len(prompt.split()) + 100
        cost = tokens * 0.00003 # Hypothetical expensive cost
        return f"[GPT-4o] Processed complex request: {prompt[:30]}...", cost, tokens
