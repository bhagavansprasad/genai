# Helper function to load images from the given url
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

multimodal_model = GenerativeModel("gemini-1.5-pro-001")
multimodal_model_flash = GenerativeModel("gemini-1.5-flash-001")

image_glasses1_url = "https://storage.googleapis.com/github-repo/img/gemini/multimodality_usecases_overview/glasses1.jpg"
image_glasses2_url = "https://storage.googleapis.com/github-repo/img/gemini/multimodality_usecases_overview/glasses2.jpg"

prompt = """
I have an oval face. Given my face shape, which glasses would be more suitable?

Explain how you reached this decision.
Provide your recommendation based on my face shape, and please give an explanation for each.
"""
image_glasses1 = load_image_from_url(image_glasses1_url)
image_glasses2 = load_image_from_url(image_glasses2_url)

contents = [prompt, image_glasses1, image_glasses2]
responses = multimodal_model.generate_content(contents)
print(responses.text)