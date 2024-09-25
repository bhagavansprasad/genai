import http.client
import typing
import urllib.request
from vertexai.generative_models import Image
from vertexai.generative_models import GenerativeModel

def get_image_bytes_from_url(image_url: str) -> bytes:
    with urllib.request.urlopen(image_url) as response:
        response = typing.cast(http.client.HTTPResponse, response)
        image_bytes = response.read()
    return image_bytes


def load_image_from_url(image_url: str) -> Image:
    image_bytes = get_image_bytes_from_url(image_url)
    return Image.from_bytes(image_bytes)

def count_people_in_image():
    img_url = "https://storage.googleapis.com/bhagavan-pub-bucket/g1.jpeg"
    image1 = load_image_from_url(img_url)

    print(image1)
    prompt = """
    I have an image loaded.
    Can you count number of people in the image also give me the count based on male, female and kids
    """

    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    contents = [prompt, image1]
    
    response = multimodal_model.generate_content(contents)
    print(f"response :{response.text}")


def count_people_in_both_images():
    img_url1 = "https://storage.googleapis.com/bhagavan-pub-bucket/g1.jpeg"
    image1 = load_image_from_url(img_url1)

    img_url2 = "https://storage.googleapis.com/bhagavan-pub-bucket/cuple.jpeg"
    image2 = load_image_from_url(img_url2)

    prompt = """
    From given two images,
    Can you count number of people in both images, and are they same people?
    """

    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    
    contents = [prompt, image1, image2]
    
    response = multimodal_model.generate_content(contents)
    print(f"response :{response.text}")


    
def main():
    # count_people_in_image()
    count_people_in_both_images()

   
if __name__ == "__main__":
    main()
