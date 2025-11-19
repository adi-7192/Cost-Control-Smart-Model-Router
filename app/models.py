from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from .database import Base

# --- Database Models ---
class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    prompt_preview = Column(String) # Store first N chars
    difficulty = Column(String)
    reasoning = Column(String) # New field
    model_used = Column(String)
    cost = Column(Float)
    tokens_used = Column(Integer)
    response_time_ms = Column(Float)

# --- Pydantic Models ---
class PromptRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100

class RouteResponse(BaseModel):
    model: str
    difficulty: str
    reasoning: str # New field
    response: str
    cost: float
    tokens: int
    latency_ms: float
