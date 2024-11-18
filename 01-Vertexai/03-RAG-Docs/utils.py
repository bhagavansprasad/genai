from globals import text_embedding_model
import numpy as np
from pprint import pprint
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

# Add colors to the print
class Color:
    """
    This class defines a set of color codes that can be used to print text in different colors.
    This will be used later to print citations and results to make outputs more readable.
    """

    PURPLE: str = "\033[95m"
    CYAN: str = "\033[96m"
    DARKCYAN: str = "\033[36m"
    BLUE: str = "\033[94m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    RED: str = "\033[91m"
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    END: str = "\033[0m"


def smart_print_with_list_trimming(dictionary, max_item_length=20, max_list_items=5):
    def trim_value(value):
        if isinstance(value, dict):  # Handle nested dictionaries
            return {k: trim_value(v) for k, v in value.items()}
        elif isinstance(value, list):  # Trim list items and limit list length
            return [trim_value(v) for v in value[:max_list_items]]
        elif isinstance(value, str) and len(value) > max_item_length:  # Trim long strings
            return value[:max_item_length] + "..."
        else:
            return value

    trimmed_dict = {k: trim_value(v) for k, v in dictionary.items()}
    pprint(trimmed_dict)

def print_text_to_text_citation(
    final_text: Dict[int, Dict[str, Any]],
    print_top: bool = True,
    chunk_text: bool = True,
) -> None:
    """
    Prints a formatted citation for each matched text in a dictionary.

    Args:
        final_text: A dictionary containing information about matched text passages,
                    with keys as text number and values as dictionaries containing
                    page number, cosine similarity score, chunk number (optional),
                    chunk text (optional), and page text (optional).
        print_top: A boolean flag indicating whether to only print the first citation (True) or all citations (False).
        chunk_text: A boolean flag indicating whether to print individual text chunks (True) or the entire page text (False).

    Returns:
        None (prints formatted citations to the console).
    """

    color = Color()

    # Iterate through the matched text citations
    for textno, text_dict in final_text.items():
        # Print the citation header
        print(color.RED + f"Citation {textno + 1}:", "Matched text: " + color.END)

        # Print the cosine similarity score
        print(color.BLUE + "score: " + color.END, text_dict["cosine_score"])

        # Print the file_name
        print(color.BLUE + "file_name: " + color.END, text_dict["file_name"])

        # Print the page number
        print(color.BLUE + "page_number: " + color.END, text_dict["page_num"])

        # Print the matched text based on the chunk_text argument
        if chunk_text:
            # Print chunk number and chunk text
            print(color.BLUE + "chunk_number: " + color.END, text_dict["chunk_number"])
            print(color.BLUE + "chunk_text: " + color.END, text_dict["chunk_text"])
        else:
            # Print page text
            print(color.BLUE + "page text: " + color.END, text_dict["page_text"])

        # Only print the first citation if print_top is True
        if print_top and textno == 0:
            break
        print()

def get_text_embedding_from_text_embedding_model(text, return_array = False):
    embeddings = text_embedding_model.get_embeddings([text])

    emb_len = len(embeddings)
    emb_values = [embedding.values for embedding in embeddings]
    text_embedding = emb_values[0]              # Debug [0]

    if return_array:
        text_embedding = np.fromiter(text_embedding, dtype=float)

    # returns 768 dimensional array
    return text_embedding

def get_cosine_score(dataframe, column_name, input_text_embed):
    emb1 = dataframe[column_name]
    emb2 = input_text_embed
    retval = np.dot(dataframe[column_name], input_text_embed)
    text_cosine_score = round(retval, 2)
    return text_cosine_score

def print_text_to_image_citation(final_images: Dict[int, Dict[str, Any]], print_top: bool = True) -> None:
    """
    Prints a formatted citation for each matched image in a dictionary.

    Args:
        final_images: A dictionary containing information about matched images,
                    with keys as image number and values as dictionaries containing
                    image path, page number, page text, cosine similarity score, and image description.
        print_top: A boolean flag indicating whether to only print the first citation (True) or all citations (False).

    Returns:
        None (prints formatted citations to the console).
    """

    color = Color()

    print()
    # Iterate through the matched image citations
    for imageno, image_dict in final_images.items():
        # Print the citation header
        print(
            color.RED + f"Citation {imageno + 1}:",
            "Matched image path, page number and page text: " + color.END,
        )

        # Print the cosine similarity score
        print(color.BLUE + "score: " + color.END, image_dict["cosine_score"])

        # Print the file_name
        print(color.BLUE + "file_name: " + color.END, image_dict["file_name"])

        # Print the image path
        print(color.BLUE + "path: " + color.END, image_dict["img_path"])

        # Print the page number
        print(color.BLUE + "page number: " + color.END, image_dict["page_num"])

        # Print the page text
        print(
            color.BLUE + "page text: " + color.END, "\n".join(image_dict["page_text"])
        )

        # Print the image description
        print(
            color.BLUE + "image description: " + color.END,
            image_dict["image_description"],
        )

        # Only print the first citation if print_top is True
        if print_top and imageno == 0:
            break
