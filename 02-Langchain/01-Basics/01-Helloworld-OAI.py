from langchain_openai import ChatOpenAI

from langchain.schema import HumanMessage

# Initialize Chat Model
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo")

# Send a message
response = chat_model.invoke([HumanMessage(content="Hello, LangChain!")])

# Print the response
print(response.content)
