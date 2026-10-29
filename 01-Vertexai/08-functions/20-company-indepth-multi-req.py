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

    get_stock_price = FunctionDeclaration(
        name="get_stock_price",
        description="Fetch the current stock price of a given company",
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol for a company",
                }
            },
        },
    )

    get_company_overview = FunctionDeclaration(
        name="get_company_overview",
        description="Get company details and other financial data",
        parameters={
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol for a company",
                }
            },
        },
    )

    get_company_news = FunctionDeclaration(
        name="get_company_news",
        description="Get the latest news headlines for a given company.",
        parameters={
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "string",
                    "description": "Stock ticker symbol for a company",
                }
            },
        },
    )

    get_news_with_sentiment = FunctionDeclaration(
        name="get_news_with_sentiment",
        description="Gets live and historical market news and sentiment data",
        parameters={
            "type": "object",
            "properties": {
                "news_topic": {
                    "type": "string",
                    "description": """News topic to learn about. Supported topics
                                include blockchain, earnings, ipo,
                                mergers_and_acquisitions, financial_markets,
                                economy_fiscal, economy_monetary, economy_macro,
                                energy_transportation, finance, life_sciences,
                                manufacturing, real_estate, retail_wholesale,
                                and technology""",
                },
            },
        },
    )

    company_insights_tool = Tool(
        function_declarations=[
            get_stock_price,
            get_company_overview,
            get_company_news,
            get_news_with_sentiment,
        ],
    )

    dump_function_tool_details(company_insights_tool.to_dict())
    
    return company_insights_tool

def get_stock_price_from_api(content):
    whoami()
    print(f"Invoking external API...content :{content}")

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={content['ticker']}&apikey={ALPHA_VANTAGE_KEY}"
    print(f"\tRequesting URL: {url}")

    api_request = requests.get(url)
    return api_request.text

def get_company_overview_from_api(content):
    whoami()
    print(f"Invoking external API...content :{content}")

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={content['ticker']}&apikey={ALPHA_VANTAGE_KEY}"
    print(f"\tRequesting URL: {url}")

    api_response = requests.get(url)

    try: #Try to convert to json. if not json return as text
        api_response_json = api_response.json()
        return {"content": api_response_json} #Correct format for function response
    except ValueError:
        return {"content": api_response.text} #If not json, return as text

def get_company_news_from_api(content):
    whoami()
    print(f"Invoking external API...content :{content}")

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={content['tickers']}&limit=20&sort=RELEVANCE&apikey={ALPHA_VANTAGE_KEY}"
    print(f"\tRequesting URL: {url}")

    api_response = requests.get(url)
    return api_response.text

def get_news_with_sentiment_from_api(content):
    whoami()
    print(f"Invoking external API...content :{content}")

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={content['news_topic']}&limit=20&sort=RELEVANCE&apikey={ALPHA_VANTAGE_KEY}"
    print(f"\tRequesting URL: {url}")

    api_request = requests.get(url)
    return api_request.text

function_handler = {
    "get_stock_price": get_stock_price_from_api,
    "get_company_overview": get_company_overview_from_api,
    "get_company_news": get_company_news_from_api,
    "get_news_with_sentiment": get_news_with_sentiment_from_api,
}

def send_chat_message(chat, prompt):
    print(f"#### Prompt: {prompt}\n")
    prompt += """
    Give a concise, high-level summary. Only use information that you learn from 
    the API responses. 
    """

    # Send a chat message to the Gemini API
    print(f"Sending message...")
    response = chat.send_message(prompt)

    print()
    print("Got response from LLM:")
    # whereami(f"response :{response}")
    # Handle cases with multiple chained function calls
    function_calling_in_process = True

def _extract_function_call(response):
    """Extracts the function call from the response."""
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                return part.function_call
    return None

def _invoke_api_function(function_name, params):
    """Invokes the appropriate API function."""
    print(f"Invoking external API from function: {function_name}...")
    function_api_response = function_handler[function_name](params)
    print(f"API response...")
    if isinstance(function_api_response["content"], dict):
        print(f"\t{str(function_api_response['content'])[:500]}...")
    else:
        print(f"\t{function_api_response['content'][:500]}...")
    return function_api_response

def _send_response_to_llm(chat, function_name, function_api_response, first_function_call):
    """Sends the API response back to the LLM."""
    if first_function_call:
        print(f"Sending API response back to LLM (Gemini) (First Call)...")
        return chat.send_message(
            Part.from_text(f"```json\n{json.dumps(function_api_response['content'])}\n```"),
        )
    else:
        print(f"Sending API response back to LLM (Gemini) (Subsequent Call)...")
        return chat.send_message(
            Part.from_function_response(
                name=function_name,
                response=function_api_response,
            ),
        )

def _process_function_call(chat, function_call, first_function_call):
    """Processes a single function call and sends the response back to the LLM."""

    function_name = function_call.name
    params = {key: value for key, value in function_call.args.items()}
    print(f"Parameters: {params}\n")

    function_api_response = _invoke_api_function(function_name, params)
    return _send_response_to_llm(chat, function_name, function_api_response, first_function_call)


def _handle_no_function_call(response):
    """Handles the case where there's no function call in the response."""
    print(f"No function call found in response.")
    return False  # Stop function calling loop

def _handle_unknown_function(function_call):
    """Handles the case of an unknown function name."""
    print(f"Function name '{function_call.name}' not found in handler.")
    return False  # Stop function calling loop

def _process_llm_response(chat, response, first_function_call):
    """Processes the LLM's response within the function calling loop."""

    function_call = _extract_function_call(response)

    if function_call:
        if function_call.name in function_handler.keys():
            response = _process_function_call(chat, function_call, first_function_call)
            return response, False  # Response and continue loop (but first call is done)
        else:
            return response, _handle_unknown_function(function_call) #Response and stop loop
    else:
        return response, _handle_no_function_call(response) #Response and stop loop

def send_chat_message(chat, prompt):
    print(f"#### Prompt: {prompt}")
    print("-" * 80)
    prompt += """
    Give a concise, high-level summary. Only use information that you learn from 
    the API responses. 
    """

    print(f"Sending initial message...")
    # response = chat.send_message(prompt, tools=[chat.tools[0]])
    response = chat.send_message(prompt)

    print()
    print("Got response from LLM:")

    function_calling_in_process = True
    first_function_call = True

    while function_calling_in_process:
        response, function_calling_in_process = _process_llm_response(chat, response, first_function_call)
        first_function_call = False #Set to false after first iteration

    print(f"Natural language response")
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        final_reply = response.text.replace("$", "\\$")
        print(f"{final_reply}")
    else:
        print(f"Unexpected final response format.")
        print(response)

def main():
    company_insights_tool = declare_fun_tool()

    MODEL = "gemini-1.5-pro-001"
    CONFIG = GenerationConfig(temperature=0)
    
    print(f"Initializing Model: {MODEL}")
    print()

    model = GenerativeModel(
        "gemini-1.5-pro-002",
        generation_config=CONFIG,
        tools=[company_insights_tool],
    )

    print(f"Starting chating...")
    chat = model.start_chat()

    # prompt = "What is the current stock price for Google?"
    # send_chat_message(chat, prompt)
    # print()

    # prompt = "Give me a company overview of Walmart and The Home Depot"
    # send_chat_message(chat, prompt)
    # print()

   
    prompt = "Has there been any exciting news related to real estate recently?"
    send_chat_message(chat, prompt)
    print()

if __name__ == "__main__":
    main()
