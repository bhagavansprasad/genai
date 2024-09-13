from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def process_pdf_number_of_tokens():
    file_uri = "gs://bhagavan-bucket/genai-resources/beginners-must-do.pdf"
    
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = "How many tokens can the model process?"
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)

def process_pdf_summarize():
    file_uri = "gs://bhagavan-bucket/genai-resources/beginners-must-do.pdf"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = """
    You are a professional document summarization specialist
    Please summrize the given document
    """
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)

def process_pdf_solution():
    file_uri = "gs://bhagavan-bucket/genai-resources/beginners-must-do.pdf"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = """
    You are a professional document summarization specialist
    How many section are available?
    """
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)
    
def process_pdf_titles():
    file_uri = "gs://bhagavan-bucket/genai-resources/beginners-must-do.pdf"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = """
    You are a professional document summarization specialist
    Can you suggest better titles for each section?
    """
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)

def process_pdf_improve_redability():
    file_uri = "gs://bhagavan-bucket/genai-resources/beginners-must-do.pdf"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = """
    You are a professional document summarization specialist
    Can you improve the readability and setence formation?
    """
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)

    
def main():
    # process_pdf_number_of_tokens()
    # process_pdf_summarize()
    # process_pdf_solution()
    # process_pdf_titles()
    process_pdf_improve_redability()
    
if __name__ == "__main__":
    main()
    