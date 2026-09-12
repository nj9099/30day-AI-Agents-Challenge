from langchain_core.prompts import ChatPromptTemplate
from llm import llm


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful cooking assistant."),
    ("human", "{question}")
])


prompt_value = prompt.invoke({
    "question": "What can I make with chicken and rice?"
})


print(prompt_value)