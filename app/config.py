from pydantic_settings import BaseSettings

from typing import Optional

class Settings(BaseSettings):
    CLASSIFIER_TYPE: str = "rules" # "rules" or "llm"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
