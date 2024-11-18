from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import Part
from vertexai.generative_models import Image
# import IPython.display
import typing


# Helper function to display content as video.
def display_content_as_video(content: str | Image | Part):
    if not isinstance(content, Part):
        return False
    part = typing.cast(Part, content)
    file_path = part.file_data.file_uri.removeprefix("gs://")
    video_url = f"https://storage.googleapis.com/{file_path}"
    # IPython.display.display(IPython.display.Video(video_url, width=350))


def process_walking_video():
    prompt = """
    From given video,
    what is happening?
    """

    video = Part.from_uri(
        # uri="https://storage.googleapis.com/bhagavan-pub-bucket/walking.mp4",
        uri="gs://bhagavan-pub-bucket/walking.mp4",
        mime_type="video/mp4"
    )
    # display_content_as_video(video)
    
    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video]
    responses = multimodal_model.generate_content(contents)
    
    print(responses.text)

def process_bday_video():
    prompt = """
    From given video,
    can you makeout what are they doing?
    """

    video = Part.from_uri(
        # uri="https://storage.googleapis.com/bhagavan-pub-bucket/walking.mp4",
        uri="gs://bhagavan-pub-bucket/bday.mp4",
        mime_type="video/mp4"
    )
    # display_content_as_video(video)
    
    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video]
    responses = multimodal_model.generate_content(contents)
    
    print(responses.text)

def process_amarnath_video():
    prompt = """
    From given video,
    Where is this location?
    """

    video = Part.from_uri(
        uri="gs://bhagavan-pub-bucket/anath.mp4",
        mime_type="video/mp4"
    )
    # display_content_as_video(video)
    
    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    
    contents = [prompt, video]
    responses = multimodal_model.generate_content(contents)
    
    print(responses.text)
    
def main():
    # process_walking_video()
    # process_bday_video()
    process_amarnath_video()
   
if __name__ == "__main__":
    main()
