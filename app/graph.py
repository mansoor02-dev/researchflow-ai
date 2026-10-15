from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

import os
from dotenv import load_dotenv

load_dotenv()
 
from app.schema import ResearchResponse


MAX_RETRIES=2

class ResearchState(TypedDict):
    topic: str
    result: dict | None
    review_passed: bool
    review_feedback: str
    retries: int

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    temperature=0.2
)

structured_model = model.with_structured_output(ResearchResponse)

prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a research assistant.
                Explain topics clearly and accurately.
                Distinguish established facts from uncertainty.
                Do not invent citations."""
            ),
            (
                "human",
                """
                Research this topic: {topic}

                If the previous output failed review, address this feedback:
                {feedback}
                """
            ),
        ])

def generate_research(state: ResearchState) -> dict:
    """Generate or regenerate a structured research response"""
    prompt_value = prompt.invoke({
        "topic": state["topic"],
        "feedback": state.get("review_feedback", ""),
    })
    
    result = structured_model.invoke(prompt_value)
    
    return {
        "result": result.model_dump(),
        "retries": state.get("retries", 0) + 1,
    }
    
def review_research(state: ResearchState) -> dict:
    """Check basic output completeness"""
    result = state.get("result")
    
    if not result:
        return {
            "review_passed": False,
            "review_feedback": "No response is generated"
        }
    
    required_fields = [
        "summary",
        "key_points",
        "assumptions",
        "follow_up_questions"
    ]
    
    missing_fields = [
        field for field in required_fields
        if not result.get(field)
    ]
    
    if missing_fields:
        return {
            "review_passed": False,
            "review_feedback": (
                f"Populate the missing or empty fields: {missing_fields}"
            )
        }
    
    return {
        "review_passed": True,
        "review_feedback": ""
    }
    
def route_after_review(state: ResearchState) -> str:
    if state["review_passed"] == True:
        return "finish"
    elif state["retries"] >= MAX_RETRIES:
        return "finish"
    else:
        return "retry"
    

builder = StateGraph(ResearchState)

builder.add_node("generate", generate_research)
builder.add_node("review", review_research)

builder.add_edge(START, 'generate')
builder.add_edge('generate', 'review')
builder.add_conditional_edges(
    'review', 
    route_after_review,
    {
        "finish": END,
        "retry": "generate"
    },
)

research_graph = builder.compile()
    