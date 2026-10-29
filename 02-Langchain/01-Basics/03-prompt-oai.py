from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

# Initialize Chat Model
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo")

# Define a Prompt Template
prompt_template = PromptTemplate(
    input_variables=["name"],
    template="Hello {name}, welcome to LangChain! How can I assist you today?"
)

# Format the Prompt
formatted_prompt = prompt_template.format(name="Bhagavan")

# Send the formatted prompt to the chat model
response = chat_model.invoke([HumanMessage(content=formatted_prompt)])

# Print the response
print(response.content)

