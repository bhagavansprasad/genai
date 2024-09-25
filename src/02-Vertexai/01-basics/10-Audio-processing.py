from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import Part

def process_backpain_audio():
    prompt = """
    From given audio file,
    What is being dicussed or explained?
    """
    prompt = """
    Please provide a short summary and title for the audio.
    Provide chapter titles, be concise and short, no need to provide chapter summaries.
    Provide each of the chapter titles in a numbered list.
    Translate to English if required
    Do not make up any information that is not part of the audio and do not be verbose.
    """

    video = Part.from_uri(
        uri="gs://bhagavan-pub-bucket/backpain.mp3",
        mime_type="audio/mp3"
    )
   
    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video]
    responses = multimodal_model.generate_content(contents)
    
    print(responses.text)

def trnscribe_backpain_audio():
    prompt = """
    From given audio file,
    Can you please trascribe the Audio in English?
    """

    video = Part.from_uri(
        uri="gs://bhagavan-pub-bucket/backpain.mp3",
        mime_type="audio/mp3"
    )
   
    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video]
    responses = multimodal_model.generate_content(contents)
    
    print(responses.text)

def flash_trnscribe_backpain_audio():
    prompt = """
    From given audio file,
    Can you please trascribe the Audio in English and store in text file with timestamp and speaker name 'A' or 'B' and translated data
    """

    video = Part.from_uri(
        uri="gs://bhagavan-pub-bucket/backpain.mp3",
        mime_type="audio/mp3"
    )
   
    model = "gemini-1.5-flash-001"
    multimodal_model_flash = GenerativeModel(model)    
    
    contents = [prompt, video]
    responses = multimodal_model_flash.generate_content(contents)
    print(responses.text)

def main():
    # process_backpain_audio()
    # trnscribe_backpain_audio()
    print("-" * 75)
    flash_trnscribe_backpain_audio()
   
if __name__ == "__main__":
    main()
