import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="myfirstgenai-432214", location="us-central1")

def query_by_model(model_name, contents):
    multimodal_model = GenerativeModel(model_name=model_name)
    print(f"Queriyng :{model_name}")
    response = multimodal_model.generate_content(contents=contents)
    print(response)
    print()
    
    print(response.text)
    print()
    

def hello_world():
    model1 = "gemini-1.5-pro-001"
    model2 = "gemini-1.5-flash-001"
    contents = ["Explain LLM"]
    
    # query_by_model(model1, contents)
    # query_by_model(model2, contents)

    
def main():
    hello_world()
    

if __name__ == "__main__":
    main()