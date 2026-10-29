import os
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.memory import ConversationBufferMemory
import json

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
os.environ["GOOGLE_CSE_ID"] = "YOUR_GOOGLE_CSE_ID"

llm = OpenAI(temperature=0)
search = GoogleSearchAPIWrapper()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tools
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. Input should be a search query.",
    ),
    Tool(
        name="Calculate",
        func=lambda x: str(eval(x)),
        description="useful for when you need to answer questions about math. Input should be a math expression.",
    ),
    Tool(
        name="GetCityWeather",
        func=lambda city: search.run(f"weather in {city}"),
        description="Useful for getting weather information. Input is the city name.",
    )
]

# Agent
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
)

# Function Calling (Manual Approach)
def process_with_function_calling(query, memory):
    prompt = f"""
    You are a helpful assistant. You have access to the following functions: Search, Calculate, GetCityWeather.
    Previous conversation: {memory}
    User: {query}
    Respond with JSON function call or a text response.
    """
    response = llm(prompt)
    try:
        function_call = json.loads(response)
        if "function_call" in function_call:
            function_name = function_call["function_call"]["name"]
            arguments = function_call["function_call"].get("arguments", {})
            if function_name == "Search":
                return search.run(arguments.get("query"))
            elif function_name == "Calculate":
                return str(eval(arguments.get("x")))
            elif function_name == "GetCityWeather":
                return search.run(f"weather in {arguments.get('city')}")
        else:
            return response
    except (json.JSONDecodeError, KeyError, TypeError, NameError) as e:
        return f"Error: {e}"

# Example Usage
print("--- Agentic Approach ---")
print(agent_chain.run("What is the capital of France?"))
print(agent_chain.run("What is 2 + 2?"))
print(agent_chain.run("What is the weather in Paris?"))
print(agent_chain.run("What is the population of the capital of France?"))

print("\n--- Function Calling Approach ---")
memory_func_call = []
print(process_with_function_calling("What is the capital of France?", memory_func_call))
print(process_with_function_calling("What is 2 + 2?", memory_func_call))
print(process_with_function_calling("What is the weather in Paris?", memory_func_call))
print(process_with_function_calling("What is the population of the capital of France?", memory_func_call))

print("\n--- Agent Memory ---")
print(memory.load_memory_variables({}))

print("\n--- Function Calling Memory ---")
print(memory_func_call)