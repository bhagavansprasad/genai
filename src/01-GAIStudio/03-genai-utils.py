import google.generativeai as genai
import os
import sys
import logging

# logging.get_absl_handler().python_handler.stream = sys.stdout

def get_gai_models():
    models = genai.list_models()

    for i, model in enumerate(models, 1):
        print(f"{i}. Name : {model.name}, Display Name :{model.display_name}")


def get_answer(question):
    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(question)
    print(response.text)


def main():
    get_gai_models()
    
    # question = "Give me a statement which very opt for winner and a looser"
    # get_answer(question)
    
if __name__ == "__main__":
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])

    main()