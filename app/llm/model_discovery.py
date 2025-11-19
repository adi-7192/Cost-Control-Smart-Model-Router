import requests
import os
from typing import Optional

class ModelDiscovery:
    """Automatically discover available models from API providers"""
    
    @staticmethod
    def get_best_gemini_model(api_key: str) -> Optional[str]:
        """
        Query Google API to find the best available Gemini model.
        Preference: flash models (fast & cheap) > pro models
        """
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                return None
            
            models = response.json().get('models', [])
            
            # Filter for Gemini models that support generateContent
            gemini_models = []
            for model in models:
                name = model.get('name', '')
                methods = model.get('supportedGenerationMethods', [])
                
                if 'gemini' in name.lower() and 'generateContent' in methods:
                    gemini_models.append(name)
            
            # Preference order: flash > pro, newer versions first
            # Priority: 2.5-flash > 2.0-flash > flash-latest > 2.5-pro > pro-latest
            priority_patterns = [
                'gemini-2.5-flash',
                'gemini-2.0-flash',
                'gemini-flash-latest',
                'gemini-2.5-pro',
                'gemini-2.0-pro',
                'gemini-pro-latest'
            ]
            
            for pattern in priority_patterns:
                for model in gemini_models:
                    if pattern in model:
                        return model.replace('models/', '')
            
            # Fallback: return first available
            if gemini_models:
                return gemini_models[0].replace('models/', '')
            
            return None
            
        except Exception as e:
            print(f"Model discovery error: {e}")
            return None
    
    @staticmethod
    def get_cached_or_discover_gemini(api_key: str) -> str:
        """
        Get Gemini model with caching to avoid repeated API calls.
        Falls back to hardcoded model if discovery fails.
        """
        # Try to discover
        discovered = ModelDiscovery.get_best_gemini_model(api_key)
        
        if discovered:
            print(f"✓ Auto-discovered Gemini model: {discovered}")
            return discovered
        
        # Fallback to known working model
        fallback = "gemini-2.5-flash"
        print(f"⚠ Model discovery failed, using fallback: {fallback}")
        return fallback
