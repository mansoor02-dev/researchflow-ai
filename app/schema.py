from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    
class ResearchResponse(BaseModel):
    topic: str
    summary: str = Field(description="Summary of the research")
    key_points: list[str] = Field(description="Key research findings")
    assumptions: str = Field(
        description="Assumptions made, under 400 characters"
    )
    follow_up_questions: list[str] = Field(
        description="Suggested follow-up questions"
    )
