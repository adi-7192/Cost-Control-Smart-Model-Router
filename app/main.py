import os
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import engine, Base, get_db
from .models import PromptRequest, RouteResponse, RequestLog
from .router import ModelRouter

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cost-Control Smart Model Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = ModelRouter()

@app.post("/route", response_model=RouteResponse)
async def route_prompt(request: PromptRequest, db: Session = Depends(get_db)):
    try:
        result = await router.route_and_execute(request.prompt, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    logs = db.query(RequestLog).all()
    total_cost = sum(log.cost for log in logs)
    total_requests = len(logs)
    
    # Group by model
    breakdown = {}
    for log in logs:
        if log.model_used not in breakdown:
            breakdown[log.model_used] = {"count": 0, "cost": 0.0}
        breakdown[log.model_used]["count"] += 1
        breakdown[log.model_used]["cost"] += log.cost
        
    return {
        "total_requests": total_requests,
        "total_cost_usd": total_cost,
        "breakdown": breakdown
    }

class KeyConfig(BaseModel):
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

@app.post("/config/keys")
def update_keys(config: KeyConfig):
    env_path = ".env"
    
    # 1. Update os.environ for immediate use
    if config.OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
    if config.GOOGLE_API_KEY:
        os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY
        
    # 2. Update .env file for persistence
    # Read existing lines
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    else:
        lines = []
        
    new_lines = []
    # Track which keys we've handled
    keys_to_update = {}
    if config.OPENAI_API_KEY: keys_to_update["OPENAI_API_KEY"] = config.OPENAI_API_KEY
    if config.GOOGLE_API_KEY: keys_to_update["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY
    
    updated_keys = set()
    
    for line in lines:
        key_match = False
        for key, value in keys_to_update.items():
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}\n")
                updated_keys.add(key)
                key_match = True
                break
        if not key_match:
            new_lines.append(line)
            
    # Append new keys if they weren't found
    for key, value in keys_to_update.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={value}\n")
        
    with open(env_path, "w") as f:
        f.writelines(new_lines)
        
    return {"status": "success", "message": "API keys updated successfully."}

@app.get("/logs")
def get_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(RequestLog).order_by(RequestLog.timestamp.desc()).limit(limit).all()
    return logs
