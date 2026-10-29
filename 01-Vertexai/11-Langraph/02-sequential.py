from langgraph.graph import StateGraph, END

# Define nodes (functions)
def summarize_text(state):
    text = state["text"]
    summary = f"Summary of: {text}"  # Replace with actual summarization logic
    return {"summary": summary}

def translate_summary(state):
    summary = state["summary"]
    translation = f"Translated: {summary}" # Replace with actual translation logic
    return {"translation": translation}

# Create the graph (NO input/output schemas)
graph = StateGraph()  # Correct: No schema arguments

graph.add_node("summarize", summarize_text)
graph.add_node("translate", translate_summary)
graph.add_edge("summarize", "translate")
graph.add_edge("translate", END)
graph.set_entry_point("summarize")

# Run the graph
initial_state = {"text": "This is a long piece of text that needs to be processed."}
final_state = graph.run(initial_state)

print(final_state["translation"])