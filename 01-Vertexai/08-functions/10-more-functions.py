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

def is_even(numbers):
    numbers = list(numbers)
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list of integers")

    results = [num % 2 == 0 for num in numbers]
    print(f"Calling is_even({numbers}) = {results}")
    return results

def is_prime(numbers):  # Local is_prime function
    # whereami(f"numbers :{numbers}")
    # whereami(f"numbers :{type(numbers)}")
    # whereami(f"numbers :{list(numbers)}")
    numbers = list(numbers)
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list of integers")

    def _is_prime(n):  
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    results = [_is_prime(num) for num in numbers]
    print(f"Calling is_prime({numbers}) = {results}")
    return results

def extract_function_call(response):
    if response.candidates[0].content.parts[0].function_call:
        return response.candidates[0].content.parts[0].function_call
    return None

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

    is_prime_func = FunctionDeclaration(  
        name="is_prime",
        description="Checks if a list of numbers are prime.",
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

    math_tool = Tool(function_declarations=[is_even_func, is_prime_func],)

    return [math_tool]

def execute_function(function_name, numbers):
    if function_name == "is_even":
        return is_even(numbers)
    elif function_name == "is_prime":  
        return is_prime(numbers)
    else:
        raise ValueError("Unknown function called.")


def generate_followup_prompt(result, prompt):
    return f"""The results are: {result}, against the prompt '{prompt}', is it true?, 
            Say in the dictionary format number: 'Even/Odd/Prime' very briefly, no explanation required"""

def handle_followup_response(followup_response):
    print("Model's final response:", followup_response.candidates[0].content.parts[0].text)
    return followup_response


def call_model(model, prompt, tools=None):
    print(f"=============={prompt}==============")
    return model.generate_content(prompt, tools=tools)


def call_model_and_execute_tools(model, tools, prompt):
    response = call_model(model, prompt, tools=tools)
    function_call = extract_function_call(response)

    if function_call:
        function_name = function_call.name
        arguments = {key: value for key, value in function_call.args.items()}

        print(f"function_call :...\n{function_call}")
        print(f"function_name :{function_name}")
        print(f"arguments     :{arguments}")

        try:
            numbers = arguments["numbers"]
            results = {}  

            even_results = is_even(numbers)
            for i, num in enumerate(numbers):
                if even_results[i]:
                    results[num] = "Even"
                else:
                    results[num] = "Odd"
                    if is_prime([num])[0]:  
                        results[num] += "/Prime"

            followup_prompt = generate_followup_prompt(results, prompt)
            followup_response = call_model(model, followup_prompt)
            return handle_followup_response(followup_response)

        except (ValueError, TypeError) as e:
            error_message = f"Error: {e}"
            print(error_message)
            return error_message

    return response.text


def main():
    model = GenerativeModel(MODEL, generation_config=CONFIG)
    tools = declare_fun_tools()

    prompt = "From following numbers 4 7 nine and 19 what are the even and prime numbers?"
    final_response = call_model_and_execute_tools(model, tools, prompt)

if __name__ == "__main__":
    main()