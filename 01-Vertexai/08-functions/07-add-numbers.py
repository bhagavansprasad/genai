from pdbwhereami import whereami
from vertexai.generative_models import (
    Content,
    GenerationConfig,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)

from google.cloud import aiplatform


model = GenerativeModel("gemini-1.5-pro-001", generation_config=GenerationConfig(temperature=0))

def declare_tools():
    add_numbers_func = FunctionDeclaration(
        name="add_numbers",
        description="Adds two numbers together.",
        parameters={
            "type": "object",
            "properties": {
                "num1": {
                    "type": "number",
                    "description": "The first number."
                },
                "num2": {
                    "type": "number",
                    "description": "The second number."
                }
            },
            "required": ["num1", "num2"]
        },
    )


    add_numbers_tool = Tool(
        function_declarations=[add_numbers_func],
    )
    
    return add_numbers_tool

def add_numbers(num1, num2):
    """Adds two numbers."""
    result = num1 + num2
    print(f"Calling add_numbers({num1}, {num2}) = {result}")
    return result


def call_model_and_execute_tools(tool, prompt):
    response = model.generate_content(
        prompt,
        tools=[tool],
    )

    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        arguments = {key: value for key, value in function_call.args.items()}
        
        whereami(f"function_call :...\n{function_call}")
        whereami(f"function_name :{function_name}")
        whereami(f"arguments     :{arguments}")

        if function_name == "add_numbers":
            num1 = float(arguments["num1"])
            num2 = float(arguments["num2"])
            result = add_numbers(num1, num2)

            followup_prompt = f"The result of add_numbers is: {result}, provide me brief summary"
            followup_response = model.generate_content(followup_prompt)
            print("Model's final response:", followup_response.candidates[0].content.parts[0].text)
            return followup_response
        else:
            return "Unknown function called."
    else:
        return response


def main():  # The main function
    tool = declare_tools()
    prompt1 = "What is 5 plus 10?"
    final_response1 = call_model_and_execute_tools(tool, prompt1)

if __name__ == "__main__":
    main()
    