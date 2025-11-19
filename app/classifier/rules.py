import re
from .base import BaseClassifier

class RuleBasedClassifier(BaseClassifier):
    def classify(self, prompt: str) -> tuple[str, str]:
        length = len(prompt)
        
        # Complex keywords/patterns
        complex_patterns = [
            r"code", r"python", r"function", r"class", # Coding tasks
            r"analyze", r"summarize", r"compare", # Analytical tasks
            r"quantum", r"physics", r"mathematics" # Domain specific
        ]
        
        if length > 500:
            return "complex", f"Prompt length ({length} chars) exceeds 500."
        
        for pattern in complex_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return "moderate", f"Contains complex keyword/pattern: '{pattern}'"
                
        if length > 100:
            return "moderate", f"Prompt length ({length} chars) exceeds 100."
            
        return "simple", "Short prompt with no complex keywords."
