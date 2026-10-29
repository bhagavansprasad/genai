from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

model = init_chat_model("gpt-4o-mini", model_provider="openai")
model.invoke([HumanMessage(content="Hi! I'm Bob")])

reply = model.invoke([HumanMessage(content="What's my name?")])
print(reply.content)

