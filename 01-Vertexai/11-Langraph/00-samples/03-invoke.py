from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from IPython.display import Image, display

class State(TypedDict):
    messages: Annotated[list, add_messages]

builder = StateGraph(State)

def chatbot(state: State):
    state["messages"].append(("assistant", "Hello"))  # Update state IN-PLACE
    return state  # Return the modified state (important!)

builder.add_node("chatbot", chatbot)
builder.set_entry_point("chatbot")
builder.set_finish_point("chatbot")
graph = builder.compile()

retval = graph.invoke({"messages": []}) 
print(retval)
print(type(graph))

try:
    # display(Image(graph.get_graph().draw_mermaid_png()))
    display(Image(graph.get_graph().draw_ascii()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
