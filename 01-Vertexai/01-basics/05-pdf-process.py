from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def process_pdf_summarize():
    file_uri = "gs://bhagavan-pub-bucket/genai-resources/BeginnersMustDoPython.pdf"
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
    file_uri = "gs://bhagavan-pub-bucket/genai-resources/BeginnersMustDoPython.pdf"
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
    file_uri = "gs://bhagavan-pub-bucket/genai-resources/BeginnersMustDoPython.pdf"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = """
    You are a professional document summarization specialist
    The existing title is not very catchie.
    I need better titles for each sectionst in markdown format?
    """
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)

def process_pdf_sections_01():
    file_uri = "gs://bhagavan-pub-bucket/genai-resources/BeginnersMustDoPython.pdf"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = """
    You are a professional document summarization specialist
    The existing title for section 1 is not very catchie.
    I need better title
    Also, repharse and the section1 and in more readable format
    Make sure output is in markdown format
    """
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)

def process_pdf_sections_05():
    file_uri = "gs://bhagavan-pub-bucket/genai-resources/BeginnersMustDoPython.pdf"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    prompt = """
    You are a professional document summarization specialist
    The existing title for section 5 is not very catchie.
    I need better title
    Also, repharse and the section5 and in more readable format
    Also, Provide and example input and expected for each problem
    Make sure output is in markdown format
    """
    
    model = "gemini-1.5-pro-001"
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model)

    response = multimodal_model.generate_content(contents=contents)
    print(response.text)

    
def main():
    # process_pdf_summarize()
    # process_pdf_solution()
    # process_pdf_titles()
    # process_pdf_improve_redability()
    # process_pdf_sections_01()
    process_pdf_sections_05()
    
if __name__ == "__main__":
    main()
    