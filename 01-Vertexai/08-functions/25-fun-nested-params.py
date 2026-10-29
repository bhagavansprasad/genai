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

    create_product_listing = FunctionDeclaration(
        name="create_product_listing",
        description="Create a product listing using the details provided by the user",
        parameters={
            "type": "object",
            "properties": {
                "product": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "brand": {"type": "string"},
                        "price": {"type": "number"},
                        "category": {"type": "string"},
                        "description": {"type": "string"},
                        "colors": {
                            "type": "object",
                            "properties": {
                                "color": {"type": "number"},
                            },
                        },
                    },
                }
            },
        },
    )

    product_listing_tool = Tool(
        function_declarations=[create_product_listing],
    )

    dump_function_tool_details(product_listing_tool.to_dict())
    
    return product_listing_tool


def main():
    print("============NOT WORKING==================")
    exit(1)
    destination_tool  = declare_fun_tool()

    MODEL = "gemini-1.5-pro-001"
    CONFIG = GenerationConfig(temperature=0)
    
    print(f"Initializing Model: {MODEL}")
    print()

    model = GenerativeModel(MODEL, generation_config=CONFIG)

    prompt = """
    Create a listing for noise-canceling headphones for $149.99.
    These headphones create a distraction-free environment.
    Available colors include black, white, and red.
    """
    
    prompt = """Create a listing:
    ```json
    {
    "product": {
        "name": "Noise-Canceling Headphones",
        "price": "$149.99",
        "description": "Create a distraction-free environment.",
        "available_colors": ["black", "white", "red"]
        }
    }
    """
    print(f"#### Prompt: {prompt}\n")
    response = model.generate_content(prompt, tools=[destination_tool])
    print(response.candidates[0].function_calls)
    
    print()

if __name__ == "__main__":
    main()
