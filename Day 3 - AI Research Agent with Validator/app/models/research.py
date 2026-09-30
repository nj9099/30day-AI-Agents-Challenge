from pydantic import BaseModel, Field, model_validator

class ResearchIntent(BaseModel):
    topic: str = Field(description="The main research topic without the time period")

    year: int | None = Field(
        default=None,
        description="The specific year requested by the user. "
        "Use None if no specific year was requested.",
    )

    is_latest: bool = Field(
        description="True only when the user explicitly asks for the latest, "
        "current, recent, or up-to-date information. "
        "If a specific year is requested, this must be False."
    )

    @model_validator(mode="after")
    def validate_time_period(self):
        if self.year is not None:
            self.is_latest = False

        return self

class ResearchValidation(BaseModel):
    valid: bool
    reason: str
    missing_information: str

class ResearchQueryRefinement(BaseModel):
    refined_query: str = Field(
        description="An improved web search query that addresses the missing information identified during research validation."
    )
