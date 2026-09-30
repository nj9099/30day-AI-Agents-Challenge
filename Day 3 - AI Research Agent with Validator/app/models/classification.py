from typing import Literal

from pydantic import BaseModel, Field

class Classification(BaseModel):
    complexity: Literal["simple", "complex"] = Field(
        description="Whether the question is simple or complex"
    )


class ToolClassification(BaseModel):
    isToolNeeded: Literal["yes", "no"] = Field(
        description="Whether the question is an arithemetic problem"
    )


class ResearchClassification(BaseModel):
    isResearch: Literal["yes", "no"] = Field(
        description="Whether the user's question requires web research"
    )

class ResearchQueryRefinement(BaseModel):
    refined_query: str = Field(
        description="An improved web search query that addresses the missing information identified during research validation."
    )

