import asyncio
import os
from app.config import settings
from app.router import ModelRouter
from app.classifier.llm import LLMClassifier
from app.classifier.rules import RuleBasedClassifier

async def verify_config():
    print(f"Current Config CLASSIFIER_TYPE: {settings.CLASSIFIER_TYPE}")
    
    router = ModelRouter()
    
    if settings.CLASSIFIER_TYPE == "llm":
        if isinstance(router.classifier, LLMClassifier):
            print("PASS: Router initialized with LLMClassifier")
        else:
            print(f"FAIL: Expected LLMClassifier, got {type(router.classifier)}")
            
        # Test classification
        difficulty = await router.classifier.classify_async("This is a hard task")
        print(f"LLM Classification Result: {difficulty}")
        if difficulty == "complex":
             print("PASS: LLM Logic correct")
        else:
             print("FAIL: LLM Logic incorrect")

    else:
        if isinstance(router.classifier, RuleBasedClassifier):
            print("PASS: Router initialized with RuleBasedClassifier")
        else:
            print(f"FAIL: Expected RuleBasedClassifier, got {type(router.classifier)}")

if __name__ == "__main__":
    asyncio.run(verify_config())
