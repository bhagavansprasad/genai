# https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/function-calling/forced_function_calling.ipynb
import os
from IPython.display import Markdown, display
import requests
import json
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)
from vertexai.preview.generative_models import ToolConfig
from pdbwhereami import whereami, whoami

ALPHA_VANTAGE_KEY = os.environ['ALPHA_VANTAGE_KEY']

def dump_function_tool_details(funct_tools):
    for ft in funct_tools['function_declarations']:
        print(f"    Name: {ft['name']}")
        print(f"    Description: {ft['description']}")
        print()

def declare_fun_tool():
    print()
    print("Initializing function tools")


    search_arxiv = FunctionDeclaration(
        name="search_arxiv",
        description="Search for articles and publications in arXiv",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Query to search for in arXiv"}
            },
        },
    )

    search_tool = Tool(function_declarations=[search_arxiv,],)  
   
    dump_function_tool_details(search_tool.to_dict())
    
    return search_tool


def main():
    destination_tool  = declare_fun_tool()

    MODEL = "gemini-1.5-pro-001"
    CONFIG = GenerationConfig(temperature=0)
    
    print(f"Initializing Model: {MODEL}")
    print()

    model = GenerativeModel(MODEL, generation_config=CONFIG)


    tool_config = ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            # mode=ToolConfig.FunctionCallingConfig.Mode.AUTO,  
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,  
        )
    )

    prompt = "Explain the Schrodinger equation in a few sentences and give me papers from arXiv to learn more"
    response = model.generate_content(prompt, tools=[destination_tool], tool_config=tool_config)
    print(f"#### Prompt: {prompt}\n")

    # print(response.candidates[0].content.parts[0].text)
    print(response.candidates[0].content.parts[0])
   
    print()

if __name__ == "__main__":
    main()
