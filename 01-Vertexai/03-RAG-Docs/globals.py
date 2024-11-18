from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import GenerativeModel
from vertexai.vision_models import MultiModalEmbeddingModel
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from vertexai.generative_models import (
    GenerationConfig,
    HarmBlockThreshold,
    HarmCategory,
    Image,
)
from vertexai.vision_models import Image as vision_model_Image

GEN_AI_MODEL = "gemini-1.5-pro-001"
text_model = GenerativeModel(GEN_AI_MODEL)
text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
multimodal_model = GenerativeModel("gemini-1.5-pro-001")
multimodal_embedding_model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")

safety_settings: Optional[dict] = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

def get_gemini_response(
    generative_multimodal_model,
    model_input: List[str],
    generation_config,
    safety_settings,
    stream: bool = True) -> str:
    """
    This function generates text in response to a list of model inputs.

    Args:
        model_input: A list of strings representing the inputs to the model.
        stream: Whether to generate the response in a streaming fashion (returning chunks of text at a time) or all at once. Defaults to False.

    Returns:
        The generated text as a string.
    """
    response = generative_multimodal_model.generate_content(
        model_input,
        generation_config=generation_config,
        stream=stream,
        safety_settings=safety_settings,
    )
    response_list = []

    for chunk in response:
        try:
            response_list.append(chunk.text)
        except Exception as e:
            print(
                "Exception occurred while calling gemini. Something is wrong. Lower the safety thresholds [safety_settings: BLOCK_NONE ] if not already done. -----",
                e,
            )
            response_list.append("Exception occurred")
            continue
    response = "".join(response_list)

    return response

def get_image_embedding_from_multimodal_embedding_model(
    image_uri: str,
    embedding_size: int = 512,
    text: Optional[str] = None,
    return_array: Optional[bool] = False,
) -> list:
    """Extracts an image embedding from a multimodal embedding model.
    The function can optionally utilize contextual text to refine the embedding.

    Args:
        image_uri (str): The URI (Uniform Resource Identifier) of the image to process.
        text (Optional[str]): Optional contextual text to guide the embedding generation. Defaults to "".
        embedding_size (int): The desired dimensionality of the output embedding. Defaults to 512.
        return_array (Optional[bool]): If True, returns the embedding as a NumPy array.
        Otherwise, returns a list. Defaults to False.

    Returns:
        list: A list containing the image embedding values. If `return_array` is True, returns a NumPy array instead.
    """
    # image = Image.load_from_file(image_uri)
    image = vision_model_Image.load_from_file(image_uri)
    embeddings = multimodal_embedding_model.get_embeddings(
        image=image, contextual_text=text, dimension=embedding_size
    )  # 128, 256, 512, 1408
    image_embedding = embeddings.image_embedding

    if return_array:
        image_embedding = np.fromiter(image_embedding, dtype=float)

    return image_embedding
