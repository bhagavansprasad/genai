from pdbwhereami import whereami
import os
import time
from vertexai.generative_models import (
    Content,
    GenerationConfig,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)
import re

os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

MODEL = "gemini-1.5-pro-001"
CONFIG = GenerationConfig(temperature=0)

def declare_fun_tools():
    is_even_func = FunctionDeclaration(
        name="is_even",
        description="Checks if a list of numbers are even.",
        parameters={
            "type": "object",
            "properties": {
                "numbers": {  
                    "type": "array", 
                    "items": {
                        "type": "integer",
                        "description": "A number to check."
                    },
                    "description": "The list of numbers to check."
                }
            },
            "required": ["numbers"]
        },
    )

    is_even_tool = Tool(
        function_declarations=[is_even_func],
    )

    return is_even_tool


def is_even(numbers):  # Now takes a list of numbers
    if not isinstance(numbers, list):
      raise TypeError("Input must be a list of integers")
    if not all(isinstance(num, int) for num in numbers):
      raise TypeError("All elements in the list must be integers")

    results = [num % 2 == 0 for num in numbers]
    print(f"Calling is_even({numbers}) = {results}")
    return results

def is_even(number):
    if not isinstance(number, int):
        raise TypeError("Input must be an integer")
    result = number % 2 == 0
    print(f"Calling is_even({number}) = {result}")
    return result

def extract_function_call(response):
    if response.candidates[0].content.parts[0].function_call:
        return response.candidates[0].content.parts[0].function_call
    return None

def execute_function(function_name, number):
    if function_name == "is_even":
        try:
            result = is_even(int(number))
            return result
        except (ValueError, TypeError) as e:
            raise
    else:
        raise ValueError("Unknown function called.")

def generate_followup_prompt(result, prompt):
    return f"The results of is_even are: {result}, against the prompt {prompt}, is it true?, Say Yes or No" 

def handle_followup_response(followup_response):
    print("Model's final response:", followup_response.candidates[0].content.parts[0].text)
    return followup_response

def call_model(model, prompt, tools=None):
    print(f"=============={prompt}==============")
    return model.generate_content(prompt, tools=tools)

def call_model_and_execute_tools(model, tool, prompt):
    response = call_model(model, prompt, tools=[tool])
    function_call = extract_function_call(response)

    if function_call:
        function_name = function_call.name
        arguments = {key: value for key, value in function_call.args.items()}

        print(f"function_call :...\n{function_call}")
        print(f"function_name :{function_name}")
        print(f"arguments    :{arguments}")

        try:
            args = list(arguments.items())[0][1]
            for arg in args:
                result = execute_function(function_name, arg)
                followup_prompt = generate_followup_prompt(result, " ".join([function_name, str(arg)]))
                followup_response = call_model(model, followup_prompt)
                handle_followup_response(followup_response)
                time.sleep(2)
            return followup_response
        except (ValueError, TypeError) as e:
            error_message = f"Error: {e}"
            print(error_message)
            return error_message

    print(response.text)
    return response.text

def main():
    model = GenerativeModel(MODEL, generation_config=CONFIG)

    tool = declare_fun_tools()

    prompt = "is 4 7 nine 19 are even numbers?"
    final_response = call_model_and_execute_tools(model, tool, prompt)


if __name__ == "__main__":
    main()
