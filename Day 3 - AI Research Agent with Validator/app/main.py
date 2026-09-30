from graph import build_graph

app = build_graph()

result = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What were the major advances in quantum computing in 2023?",
            }
        ],
        "research_attempts": 0,
    }
)

print("Attempts:", result["research_attempts"])
print("Query history:", result["research_query_history"])
print("Valid:", result["research_valid"])
print("Reason:", result["research_validation_reason"])
print("Missing:", result["research_missing_information"])
print("\nAnswer\n")
print(result)