import asyncio
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage

# Define a new stateful graph
workflow = StateGraph(state_schema=MessagesState)

# Initialize the chat model (OpenAI GPT-4o-mini)
model = init_chat_model("gpt-4o-mini", model_provider="openai")

# Define function to call the model
async def call_model(state: MessagesState):
    response = await model.ainvoke(state["messages"])  # ✅ Async support
    return {"messages": response}

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory for conversation history
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}

# Function to handle chat asynchronously
async def chat_with_memory():
    user_queries = [
        "Hi! I'm Bob.",
        "What's my name?",
        "Tell me something interesting about AI.",
        "Do you still remember my name?",
    ]

    for query in user_queries:
        input_messages = [HumanMessage(query)]
        output = await app.ainvoke({"messages": input_messages}, config)  # ✅ Async call
        print(f"User: {query}\nBot: {output['messages'][-1].content}\n")

    print(f"Final Conversation History:\n{output}")

# Run async function
if __name__ == "__main__":
    asyncio.run(chat_with_memory())  # ✅ Async execution
