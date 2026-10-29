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

    get_multiple_location_coordinates = FunctionDeclaration(
        name="get_location_coordinates",
        description="Get coordinates of multiple locations",
        parameters={
            "type": "object",
            "properties": {
                "locations": {
                    "type": "array",
                    "description": "A list of locations",
                    "items": {
                        "description": "Components of the location",
                        "type": "object",
                        "properties": {
                            "point_of_interest": {
                                "type": "string",
                                "description": "Name or type of point of interest",
                            },
                            "city": {"type": "string", "description": "City"},
                            "country": {"type": "string", "description": "Country"},
                        },
                        "required": [
                            "point_of_interest",
                            "city",
                            "country",
                        ],
                    },
                }
            },
        },
    )

    geocoding_tool = Tool(function_declarations=[get_multiple_location_coordinates],)

    dump_function_tool_details(geocoding_tool.to_dict())
    
    return geocoding_tool


def main():
    destination_tool  = declare_fun_tool()

    MODEL = "gemini-1.5-pro-001"
    CONFIG = GenerationConfig(temperature=0)
    
    print(f"Initializing Model: {MODEL}")
    print()

    model = GenerativeModel(MODEL, generation_config=CONFIG)

    prompt = """
        I'd like to get the coordinates for
        the Eiffel tower in Paris,
        the statue of liberty in New York,
        and Port Douglas near the Great Barrier Reef.
    """
    print(f"#### Prompt: {prompt}\n")
    response = model.generate_content(prompt, tools=[destination_tool])
    print(response.candidates[0].function_calls)
    
    print()

if __name__ == "__main__":
    main()
