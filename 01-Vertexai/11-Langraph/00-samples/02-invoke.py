from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

builder = StateGraph(State)

builder.add_node("chatbot", lambda state: {"messages": [("assistant", "Hello")]})
builder.set_entry_point("chatbot")

builder.set_finish_point("chatbot")
graph = builder.compile()

retval = graph.invoke({"messages": []})
print(retval)

