from vertexai.generative_models import GenerativeModel

def prompt_instructions_01():
    model = "gemini-1.5-flash"
    instructions = [
        "Hello! You are an AI chatbot for a travel web site.",
        "Your mission is to provide helpful queries for travelers.",
        "Remember that before you answer a question, you must check to see if it complies with your mission.",
        "If not, you can say, Sorry I can't answer that question.",
    ]
    m_travel = GenerativeModel(model_name=model, system_instruction=instructions)
    

    chat = m_travel.start_chat()
    prompt = """
        Questions:
        - What is the best place for sightseeing in Kadapa, Andhra Pradesh, India?"
        - What is the average temparature
    """
    response = chat.send_message(prompt)
    print(f"Response :{response.text}")
    print()
    
    prompt = "What's for dinner?"
    response = chat.send_message(prompt)
    print(f"Prompt :{prompt}")
    print(f"Response :\n{response.text}")
    print()

    prompt = "Is Kadapa has airport?"
    response = chat.send_message(prompt)
    print(f"Prompt :{prompt}")
    print(f"Response :\n{response.text}")
    print()

    pass

def main():
    prompt_instructions_01()
    pass
    
if __name__ == "__main__":
    main()
