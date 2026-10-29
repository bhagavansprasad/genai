# https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/function-calling/function_calling_data_structures.ipynb

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

    get_destination_params = FunctionDeclaration(
        name="get_destination_params",
        description="Get directions to a destination",
        parameters={
            "type": "object",
            "properties": {
                "destination": {
                    "type": "string",
                    "description": "Destination that the user wants to go to",
                },
                "mode_of_transportation": {
                    "type": "string",
                    "description": "Mode of transportation to use",
                },
                "departure_time": {
                    "type": "string",
                    "description": "Time that the user will leave for the destination",
                },
            },
        },
    )

    destination_tool = Tool(function_declarations=[get_destination_params],)

    dump_function_tool_details(destination_tool.to_dict())
    
    return destination_tool


def main():
    destination_tool  = declare_fun_tool()

    MODEL = "gemini-1.5-pro-001"
    CONFIG = GenerationConfig(temperature=0)
    
    print(f"Initializing Model: {MODEL}")
    print()

    model = GenerativeModel(MODEL, generation_config=CONFIG)
    prompt = "I'd like to travel to Paris by train and leave at 9:00 am"
    print(f"#### Prompt: {prompt}\n")
    
    response = model.generate_content(prompt, tools=[destination_tool])
    print(response.candidates[0].function_calls)
    
    print()

if __name__ == "__main__":
    main()
