from pdbwhereami import whereami
import time
import vertexai
import os
from vertexai.generative_models import (FunctionDeclaration,
                                        GenerativeModel,
                                        GenerationConfig,
                                        Part,
                                        Tool)


os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


PROJECT_ID = os.environ['PROJECT_ID']
LOCATION = os.environ['LOCATION_ID']

vertexai.init(project=PROJECT_ID, location=LOCATION)

def declare_functions():
    get_product_info = FunctionDeclaration(
        name="get_product_info",
        description="Get the stock amount and identifier for a given product",
        parameters={
            "type": "object",
            "properties": {
                "product_name": {"type": "string", "description": "Product name"}
            },
        },
    )

    whereami()

    get_store_location = FunctionDeclaration(
        name="get_store_location",
        description="Get the location of the closest store",
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "Location"}},
        },
    )

    whereami()

    place_order = FunctionDeclaration(
        name="place_order",
        description="Place an order",
        parameters={
            "type": "object",
            "properties": {
                "product": {"type": "string", "description": "Product name"},
                "address": {"type": "string", "description": "Shipping address"},
            },
        },
    )

    return [get_product_info, get_store_location, place_order]

def get_retail_tool():
    functions = declare_functions()
    retail_tool = Tool(function_declarations=functions)
    
    whereami()
    return retail_tool

def init_chat(model):
    retail_tool = get_retail_tool()
    config = GenerationConfig(temperature=0)
    model = GenerativeModel(model, generation_config=config, tools=[retail_tool])
    
    chat = model.start_chat()
    
    return chat


def post_question(chat, prompt):
    print()
    whereami(f"Prompt: {prompt}")
    
    response = chat.send_message(prompt)
    
    return response.candidates[0].content.parts[0]

def send_reponse_by_function(chat, response, function_name):
    response = chat.send_message(
        Part.from_function_response(
            name=function_name,
            response={
                "content": response,
            },
        ),
    )
    whereami()
    return response

def main():
    MODEL = "gemini-1.5-pro-001"
    
    chat = init_chat(MODEL)
    
    prompt = """
    I'd like to order a Pixel 8 Pro and have it shipped 6th Cross, Ambedkar Nagar, Sarjapur Road, 560035, Bengaluru, IND.
    """

    response = post_question(chat, prompt)
    whereami()
    print(response)

    api_response = {
        "payment_status": "paid",
        "order_number": 12345,
        "est_arrival": "2 days",
    }
    function_name = "place_order"
    response = send_reponse_by_function(chat, api_response, function_name)
    whereami()
    print(response.text)
    
    print()


if __name__ == "__main__":
    main()
    
