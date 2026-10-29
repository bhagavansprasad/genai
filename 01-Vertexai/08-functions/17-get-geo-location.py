from pdbwhereami import whereami
import time
import vertexai
import os
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    GenerationConfig,
    Part,
    Tool)

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"
API_KEY = os.environ['GEMINI_API_KEY']


PROJECT_ID = os.environ['PROJECT_ID']
LOCATION = os.environ['LOCATION_ID']

vertexai.init(project=PROJECT_ID, location=LOCATION)

def declare_functions():
    get_location = FunctionDeclaration(
        name="get_location",
        description="Get latitude and longitude for a given location",
        parameters={
            "type": "object",
            "properties": {
                "poi": {"type": "string", "description": "Point of interest"},
                "street": {"type": "string", "description": "Street name"},
                "city": {"type": "string", "description": "City name"},
                "county": {"type": "string", "description": "County name"},
                "state": {"type": "string", "description": "State name"},
                "country": {"type": "string", "description": "Country name"},
                "postal_code": {"type": "string", "description": "Postal code"},
            },
        },
    )

    location_tool = Tool(function_declarations=[get_location])
    
    return location_tool


def main():
    MODEL = "gemini-1.5-pro-001"
    
    location_tool = declare_functions()

    prompt = """
    I want to get the coordinates for the following address:
    1600 Amphitheatre Pkwy, Mountain View, CA 94043, US
    """
    model = LargeLanguageModel(api_key="YOUR_API_KEY") 
    config = GenerationConfig(temperature=0)
    # model = GenerativeModel(MODEL, generation_config=config, tools=[location_tool])

    response = GenerativeModel.generate_content(prompt, generation_config=config, tools=[location_tool])
    print(response.candidates[0].content.parts[0])

    print()


if __name__ == "__main__":
    print("===============NOT WORKING==============")
    exit(1)
    main()
    
