from vertexai.generative_models import GenerativeModel

def texual_data_queries_01():
    question = "What is the average weather in Bengaluru, India in the middle of December?"
    prompt = """
    Considering the weather, please provide some outfit suggestions. 

    Give examples for the daytime and the evening.
    """

    model = "gemini-1.5-pro-001"
    
    multimodal_model = GenerativeModel(model)
    contents = [question, prompt]

    response = multimodal_model.generate_content(contents)
    
    print(response.text)
    
def main():
    texual_data_queries_01()

if __name__ == "__main__":
    main()