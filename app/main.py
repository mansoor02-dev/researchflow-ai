# app/main.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.schema import ResearchRequest, ResearchResponse  # <-- Updated import
from app.graph import research_graph 

load_dotenv()

app = FastAPI(
    title='ResearchFlow AI',
    description='AI research assistant',
    version="0.1.0"
)

@app.get("/health")
def health():
    return {"status": "ok"} 

@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    if not os.getenv('GOOGLE_API_KEY'):
        raise HTTPException(
            status_code=500,
            detail="GEMINI api key is not configured"
        )
    try:
        state = research_graph.invoke({
            "topic": request.topic, 
            "result": None,
            "review_passed": False,
            "review_feedback": "",
            "retries": 0,
        })
        return state['result']
        
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=502,
            detail="The AI provider request failed.",
        )