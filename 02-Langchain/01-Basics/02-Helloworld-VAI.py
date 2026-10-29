from langchain_google_vertexai import ChatVertexAI
from langchain.schema import HumanMessage

# Initialize Vertex AI Chat Model (Gemini)
chat_model = ChatVertexAI(model_name="gemini-pro")

# Send a message
response = chat_model.invoke([HumanMessage(content="Hello, LangChain!")])

# Print the response
print(response.content)
