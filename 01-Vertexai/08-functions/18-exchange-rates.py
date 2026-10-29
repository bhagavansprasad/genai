from pdbwhereami import whereami, whoami
import os
from vertexai.generative_models import (
    Content,
    GenerationConfig,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
import requests

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

MODEL = "gemini-1.5-pro-001"
CONFIG = GenerationConfig(temperature=0)

def dump_function_tool_details(funct_tools):
    for ft in funct_tools['function_declarations']:
        print(f"    Name: {ft['name']}")
        print(f"    Description: {ft['description']}")
        print()

def declare_fun_tools():
    print("Initializing function tools")
    get_exchange_rate_func = FunctionDeclaration(
        name="get_exchange_rate",
        description="Get the exchange rate for currencies between countries",
        parameters={
            "type": "object",
            "properties": {
                "currency_date": {
                    "type": "string",
                    "description": "A date that must always be in YYYY-MM-DD format or the value 'latest' if a time period is not specified"
                },
                "currency_from": {
                    "type": "string",
                    "description": "The currency to convert from in ISO 4217 format"
                },
                "currency_to": {
                    "type": "string",
                    "description": "The currency to convert to in ISO 4217 format"
                }
            },
            "required": [
                "currency_from",
                "currency_date",
                "currency_to"
            ]
        },
    )

    tools_list = [get_exchange_rate_func]
    exchange_rate_tool = Tool(
        function_declarations=tools_list,
    )

    dump_function_tool_details(exchange_rate_tool.to_dict())

    return exchange_rate_tool

def get_exchange_rate(currency_date, currency_from, currency_to):
    try:
        url = f"https://api.frankfurter.app/{currency_date}"
        params = {"from": currency_from, "to": currency_to}
        
        print(f"\tRequesting URL: {url} with params: {params}")
        
        api_response = requests.get(url, params=params)
        api_response.raise_for_status()
        
        return api_response.text
    
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching exchange rate: {e}"
        print(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return {"error": error_message}


def extract_function_call(response):
    if response.candidates and response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
        return response.candidates[0].content.parts[0].function_call
    return None

def execute_function(function_name, arguments):
    if function_name == "get_exchange_rate":
        try:
            currency_date = arguments.get("currency_date")
            currency_from = arguments.get("currency_from")
            currency_to = arguments.get("currency_to")
            result = get_exchange_rate(currency_date, currency_from, currency_to)
            return result
        except (ValueError, TypeError) as e:
            raise
    else:
        raise ValueError("Unknown function called.")

def call_model(model, prompt, tools=None):
    print(f"Prompt: {prompt}")
    return model.generate_content(prompt, tools=tools)

def call_model_and_execute_tools(model, tool, prompt):
    print(f"Initializing Model: {MODEL}")
    print()
    response = call_model(model, prompt, tools=[tool])
    function_call = extract_function_call(response)

    if function_call:
        function_name = function_call.name
        arguments = {key: value for key, value in function_call.args.items()}

        print()
        print("Got response from LLM:")
        print(f"    Function to call: '{function_name}'")
        print("    Arguments:", arguments)
        print()

        print(f"Calling function: {function_name}...")
        try:
            return execute_function(function_name, arguments)
        except (ValueError, TypeError) as e:
            error_message = f"Error: {e}"
            print(error_message)
            return error_message

def main():
    model = GenerativeModel(MODEL, generation_config=CONFIG)

    tool = declare_fun_tools()

    prompt = """What is the exchange rate from Indian Rupees to US Dollars on 2024-08-20? 
    How much is 10000 Indian Rupees worth in US Dollars?"""
    
    final_response = call_model_and_execute_tools(model, tool, prompt)
    print()
    print(f"Final response:...\n\t{final_response}")
    print()

if __name__ == "__main__":
    main()