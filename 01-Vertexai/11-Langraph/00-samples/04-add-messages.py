from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages(format='langchain-openai')]

def chatbot_node(state: State) -> list:
    return {"messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Here's an image:",
                    "cache_control": {"type": "ephemeral"},
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": "1234",
                    },
                },
            ]
        },
    ]}
builder = StateGraph(State)
builder.add_node("chatbot", chatbot_node)
builder.set_entry_point("chatbot")
builder.set_finish_point("chatbot")
graph = builder.compile()
print(graph.invoke({"messages": []}))
