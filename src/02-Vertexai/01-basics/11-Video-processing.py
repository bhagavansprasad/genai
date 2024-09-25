from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import Part

def find_the_scene_time():
    prompt = """
    From given video file,
    Give me timestamp when there is a hi-fi by two members
    """

    video = Part.from_uri(
        uri="gs://bhagavan-pub-bucket/bday.mp4",
        mime_type="video/mp4"
    )
   
    model = "gemini-1.5-flash-001"
    multimodal_model_flash = GenerativeModel(model)    
    
    contents = [prompt, video]
    responses = multimodal_model_flash.generate_content(contents)
    print(responses.text)

def locate_image_in_video_01():
    prompt = """
    Look through each frame in the video carefully and answer the questions.
    Only base your answers strictly on what information is available in the video attached.
    Do not make up any information that is not part of the video and do not be too
    verbose, be straightforward.

    Questions:
    - When is the moment in the image happening in the video? Provide a timestamp.
    - What is the context of the moment and what does the narrator say about it?
    """
    
    video_file_uri = "gs://bhagavan-pub-bucket/surprise.mp4"
    image_file_uri = "gs://bhagavan-pub-bucket/saketh.jpg"

    video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")
    image_file = Part.from_uri(image_file_uri, mime_type="image/png")

    # model = "gemini-1.5-flash-001"
    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video_file, image_file]
    responses = multimodal_model.generate_content(contents)
    print(responses.text)

def locate_image_in_video_02():
    prompt = """
    Look through each frame in the video carefully and answer the questions.
    Only base your answers strictly on what information is available in the video attached.
    Do not make up any information that is not part of the video and do not be too
    verbose, be straightforward.
    

    Questions:
    - When is the moment in the image happening in the video? Provide a timestamp.
    - What is the context of the moment and what does the narrator say about it?
    - What is the reason, the previous response was wrong with time stamp, intead of 01:12, it gave me 00:12. 
    """
    
    video_file_uri = "gs://bhagavan-pub-bucket/surprise.mp4"
    image_file_uri = "gs://bhagavan-pub-bucket/hug.png"

    video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")
    image_file = Part.from_uri(image_file_uri, mime_type="image/png")

    # model = "gemini-1.5-flash-001"
    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video_file, image_file]
    responses = multimodal_model.generate_content(contents)
    print(responses.text)

def comment_on_the_video():
    prompt = """
    From the given the 10 years old video
    Generate fun commetory on the video
    """
    
    video_file_uri = "gs://bhagavan-pub-bucket/dance.mp4"

    video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")

    model = "gemini-1.5-flash"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video_file]
    responses = multimodal_model.generate_content(contents)
    print(responses.text)

def main():
    # find_the_scene_time()
    # locate_image_in_video_01()
    locate_image_in_video_02()
    # comment_on_the_video()
    pass
   
if __name__ == "__main__":
    main()
