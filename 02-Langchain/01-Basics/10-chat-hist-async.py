from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage
import asyncio

model = init_chat_model("gpt-4o-mini", model_provider="openai")

async def call_model(state: MessagesState):
    response = await model.ainvoke(state["messages"])
    return {"messages": response}

async def main():
    workflow = StateGraph(state_schema=MessagesState)
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    app = workflow.compile(checkpointer=MemorySaver())

    # Add memory

    config = {"configurable": {"thread_id": "abc123"}}

    query = "Hi! I'm Bob."

    input_messages = [HumanMessage(query)]
    output = await app.ainvoke({"messages": input_messages}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state


if __name__ == "__main__":
    asyncio.run(main())
