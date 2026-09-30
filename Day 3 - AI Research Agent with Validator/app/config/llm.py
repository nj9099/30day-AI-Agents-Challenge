from langchain_openai import ChatOpenAI

from models.classification import (
    Classification,
    ToolClassification,
    ResearchClassification,
    ResearchQueryRefinement
)

from models.research import ResearchIntent, ResearchValidation

from tools.research_tools import (
    calculator, word_counter, research_topic
)

# Create LLM node
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

classifier_llm = llm.with_structured_output(Classification)
tool_classifier_llm = llm.with_structured_output(ToolClassification)
research_classifier = llm.with_structured_output(ResearchIntent)
research_decision_llm = llm.with_structured_output(ResearchClassification)
research_validator = llm.with_structured_output(ResearchValidation)
research_refiner = llm.with_structured_output(ResearchQueryRefinement)

llm_with_tools = llm.bind_tools([calculator, word_counter, research_topic])
