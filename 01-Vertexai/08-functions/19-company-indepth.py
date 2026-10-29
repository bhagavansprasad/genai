import os
from IPython.display import Markdown, display
import requests
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)
from pdbwhereami import whereami

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
    print(f"Invoking external API...")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={content['ticker']}&apikey={ALPHA_VANTAGE_KEY}"

    print(f"\tRequesting URL: {url}")
    api_request = requests.get(url)
    return api_request.text

def get_company_overview_from_api(content):
    whereami()
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={content['ticker']}&apikey={ALPHA_VANTAGE_KEY}"
    api_response = requests.get(url)
    return api_response.text

def get_company_news_from_api(content):
    whereami()
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={content['tickers']}&limit=20&sort=RELEVANCE&apikey={ALPHA_VANTAGE_KEY}"
    api_response = requests.get(url)
    return api_response.text

def get_news_with_sentiment_from_api(content):
    whereami()
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={content['news_topic']}&limit=20&sort=RELEVANCE&apikey={ALPHA_VANTAGE_KEY}"
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

def send_chat_message(chat, prompt):
    print(f"#### Prompt: {prompt}")
    print("-"*80)
    prompt += """
    Give a concise, high-level summary. Only use information that you learn from 
    the API responses. 
    """

    print(f"Sending message...")
    response = chat.send_message(prompt)

    print()
    print("Got response from LLM:")
    # whereami(f"Initial response :\n{response}")  # Debug: Print initial response

    function_calling_in_process = True
    while function_calling_in_process:
        function_call = None  # Initialize to None
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call'):
                    function_call = part.function_call
                    break

        if function_call:
            print(f"Function call detected...")
            if function_call.name in function_handler.keys():
                function_name = function_call.name
                params = {key: value for key, value in function_call.args.items()}
                print(f"Parameters: {params}\n")

                print(f"Invoking external API from function: {function_name}...")
                function_api_response = function_handler[function_name](params)[:20000]
                print(f"API response...")
                # print(f"\t{function_api_response[:500]}...")
                print()

                print(f"Sending API response back to LLM (Gemini)...")
                response = chat.send_message(
                    Part.from_function_response(
                        name=function_name,
                        response={"content": function_api_response},
                    ),
                )
                # whereami(f"Response after API call:\n{response}")  # Debug: Response after API call

            else:
                print(f"Function name '{function_call.name}' not found in handler.") # Debug
                function_calling_in_process = False  # Stop if function name not found
        else:
            # print(f"{whereami()}: No function call found in response.")  # Debug
            function_calling_in_process = False  # Stop if no function call

    print(f"Natural language response")
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        final_reply = response.text.replace("$", "\\$")
        print(f"{final_reply}")
    else:
        print(f"Unexpected final response format.")
        print(response) # Print the full response for inspection    
    

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

    prompt = "What is the current stock price for Google?"
    send_chat_message(chat, prompt)
    print()


    prompt = "Give me a company overview of Walmart and The Home Depot"
    send_chat_message(chat, prompt)
    print()

    return
    
    prompt = "Has there been any exciting news related to real estate recently?"
    send_chat_message(chat, prompt)
    print()

if __name__ == "__main__":
    main()
