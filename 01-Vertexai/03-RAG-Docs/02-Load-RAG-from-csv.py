import os
import glob
import json
import pandas as pd
import numpy as np
import fitz
import time

from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import (
    GenerationConfig,
    HarmBlockThreshold,
    HarmCategory,
    Image,
)
from vertexai.vision_models import Image as vision_model_Image
from vertexai.vision_models import MultiModalEmbeddingModel

from utils import get_text_embedding_from_text_embedding_model
from utils import get_cosine_score
from utils import smart_print_with_list_trimming
from utils import print_text_to_text_citation
from utils import print_text_to_image_citation
from globals import get_gemini_response
from globals import text_model
from globals import safety_settings
from globals import get_image_embedding_from_multimodal_embedding_model

from pprint import pprint

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

def load_embeddings_from_csv(text_embeddings_csv):
    metadata_df = pd.read_csv(text_embeddings_csv)
    print(metadata_df.head()) 
    print(metadata_df.columns)
    return metadata_df

def load_embeddings_from_json(text_embeddings_json):
    metadata_df = pd.read_json(text_embeddings_json)
    print(metadata_df.head()) 
    print(metadata_df.columns)
    return metadata_df

def get_user_query_text_embeddings(user_query):
    return get_text_embedding_from_text_embedding_model(user_query)
           
def get_simular_text_from_query(query, text_metadata_df, column_name, top_n=3, chunk_text = True, print_citation = False):
    # print(text_metadata_df.columns)
    if column_name not in text_metadata_df.columns:
        raise KeyError(f"Column '{column_name}' not found in dataframe")
    
    query_vector = get_user_query_text_embeddings(query)
    
    cosine_scores = text_metadata_df.apply(
        lambda row: get_cosine_score(row, column_name, query_vector),
        axis = 1,)
    
    top_n_indices = cosine_scores.nlargest(top_n).index.tolist()
    top_n_scores = cosine_scores.nlargest(top_n).values.tolist()
    
    final_text: Dict[int, Dict[str, Any]] = {}
    
    print(f"top_n_indices :{top_n_indices}")
    print(f"top_n_scores  :{top_n_scores}")
    
    for matched_textno, index in enumerate(top_n_indices):
        # Create a sub-dictionary for each matched text
        final_text[matched_textno] = {}

        # Store page number
        final_text[matched_textno]["file_name"] = text_metadata_df.iloc[index]["file_name"]

        # Store page number
        final_text[matched_textno]["page_num"] = text_metadata_df.iloc[index]["page_num"]

        # Store cosine score
        final_text[matched_textno]["cosine_score"] = top_n_scores[matched_textno]

        if chunk_text:
            # Store chunk number
            final_text[matched_textno]["chunk_number"] = text_metadata_df.iloc[index]["chunk_number"]

            # Store chunk text
            final_text[matched_textno]["chunk_text"] = text_metadata_df["chunk_text"][index]
        else:
            # Store page text
            final_text[matched_textno]["text"] = text_metadata_df["text"][index]
    
    
    # smart_print_with_list_trimming(final_text, max_item_length=500, max_list_items=5)
    return final_text

    # print(final_text)
    pass

def get_user_query_image_embeddings(
    image_query_path: str, embedding_size: int
) -> np.ndarray:
    """
    Extracts image embeddings for the user query image using a multimodal embedding model.

    Args:
        image_query_path: The path to the user query image.
        embedding_size: The desired embedding size.

    Returns:
        A NumPy array representing the user query image embedding.
    """

    return get_image_embedding_from_multimodal_embedding_model(
        image_uri=image_query_path, embedding_size=embedding_size
    )


def get_similar_image_from_query(
    text_metadata_df: pd.DataFrame,
    image_metadata_df: pd.DataFrame,
    query: str = "",
    image_query_path: str = "",
    column_name: str = "",
    image_emb: bool = True,
    top_n: int = 3,
    embedding_size: int = 128,
) -> Dict[int, Dict[str, Any]]:
    """
    Finds the top N most similar images from a metadata DataFrame based on a text query or an image query.

    Args:
        text_metadata_df: A Pandas DataFrame containing text metadata associated with the images.
        image_metadata_df: A Pandas DataFrame containing image metadata (paths, descriptions, etc.).
        query: The text query used for finding similar images (if image_emb is False).
        image_query_path: The path to the image used for finding similar images (if image_emb is True).
        column_name: The column name in the image_metadata_df containing the image embeddings or captions.
        image_emb: Whether to use image embeddings (True) or text captions (False) for comparisons.
        top_n: The number of most similar images to return.
        embedding_size: The dimensionality of the image embeddings (only used if image_emb is True).

    Returns:
        A dictionary containing information about the top N most similar images, including cosine scores, image objects, paths, page numbers, text excerpts, and descriptions.
    """
    # Check if image embedding is used
    if image_emb:
        # Calculate cosine similarity between query image and metadata images
        user_query_image_embedding = get_user_query_image_embeddings(
            image_query_path, embedding_size
        )
        cosine_scores = image_metadata_df.apply(lambda x: get_cosine_score(x, column_name, user_query_image_embedding),  axis=1,)
    else:
        # Calculate cosine similarity between query text and metadata image captions
        user_query_text_embedding = get_user_query_text_embeddings(query)
        cosine_scores = image_metadata_df.apply(
            lambda x: get_cosine_score(x, column_name, user_query_text_embedding),
            axis=1,
        )

    # Remove same image comparison score when user image is matched exactly with metadata image
    cosine_scores = cosine_scores[cosine_scores < 1.0]

    # Get top N cosine scores and their indices
    top_n_cosine_scores = cosine_scores.nlargest(top_n).index.tolist()
    top_n_cosine_values = cosine_scores.nlargest(top_n).values.tolist()

    # Create a dictionary to store matched images and their information
    final_images: Dict[int, Dict[str, Any]] = {}

    for matched_imageno, indexvalue in enumerate(top_n_cosine_scores):
        # Create a sub-dictionary for each matched image
        final_images[matched_imageno] = {}

        # Store cosine score
        final_images[matched_imageno]["cosine_score"] = top_n_cosine_values[
            matched_imageno
        ]

        # Load image from file
        final_images[matched_imageno]["image_object"] = Image.load_from_file(
            image_metadata_df.iloc[indexvalue]["img_path"]
        )

        # Add file name
        final_images[matched_imageno]["file_name"] = image_metadata_df.iloc[indexvalue][
            "file_name"
        ]

        # Store image path
        final_images[matched_imageno]["img_path"] = image_metadata_df.iloc[indexvalue][
            "img_path"
        ]

        # Store page number
        final_images[matched_imageno]["page_num"] = image_metadata_df.iloc[indexvalue][
            "page_num"
        ]

        final_images[matched_imageno]["page_text"] = np.unique(
            text_metadata_df[
                (
                    text_metadata_df["page_num"].isin(
                        [final_images[matched_imageno]["page_num"]]
                    )
                )
                & (
                    text_metadata_df["file_name"].isin(
                        [final_images[matched_imageno]["file_name"]]
                    )
                )
            ]["page_text"].values
        )

        # Store image description
        final_images[matched_imageno]["image_description"] = image_metadata_df.iloc[
            indexvalue
        ]["img_desc"]

    return final_images

def search_in_text(query, text_df):
    matching_results_text = get_simular_text_from_query(query, text_df, column_name="text_embedding_chunk", top_n=10, chunk_text=True)
    print_text_to_text_citation(matching_results_text, print_top=False, chunk_text=True)

    # All relevant text chunk found across documents based on user query
    context = "\n".join(
        [value["chunk_text"] for key, value in matching_results_text.items()]
    )
    
    print(context)

    instruction = f"""Answer the question with the given context.
    If the information is not available in the context, just return "not available in the context".
    Question: {query}
    Context: {context}
    Answer:
    """

    # Prepare the model input
    model_input = instruction

    # Generate Gemini response with streaming output
    response = get_gemini_response(
        text_model,  # we are passing Gemini 1.0 Pro
        model_input=model_input,
        generation_config=GenerationConfig(temperature=0.2),
        safety_settings=safety_settings,        
        stream=True,
    )
    
    print(f"response :{response}")

def search_text_in_image(query, text_df, image_df):
    ####################################################################################
    # Search similar images with the text query
    ####################################################################################
    matching_results_image = get_similar_image_from_query(
        text_df,
        image_df,
        query=query,
        column_name="text_embedding_from_image_description",  # Use image description text embedding
        image_emb=False,  # Use text embedding instead of image embedding
        top_n=3,
        embedding_size=1408,
    )

    print_text_to_image_citation(matching_results_image, print_top=True)

def search_image_by_image(query, text_df, image_df, image_query_path=None):
    matching_results_image = get_similar_image_from_query(
        text_df,
        image_df,
        query=query,  # Use query text for additional filtering (optional)
        column_name="mm_embedding_from_img_only",  # Use image embedding for similarity calculation
        image_emb=True,
        image_query_path=image_query_path,  # Use input image for similarity calculation
        top_n=3,  # Retrieve top 3 matching images
        embedding_size=1408,  # Use embedding size of 1408
    )

    print("done")

    print_text_to_image_citation(
        matching_results_image, print_top=True
    )
    

def main():
    text_embeddings_csv = 'rag_data/docs_text.csv'
    image_embeddings_csv = 'rag_data/docs_image.csv'

    text_embeddings_json = 'rag_data/docs_text.json'
    image_embeddings_json = 'rag_data/docs_image.json'
 
    text_df = load_embeddings_from_json(text_embeddings_json)
    image_df = load_embeddings_from_json(image_embeddings_json)

    query = "Get me infomation on file operations in both C and Python"
    query = "Functions"
    query = "PgSQL"
    query = "Python Programming"
    query = "Get me infomation on file operations in both C and Python"
    query = "Bit Manipulations"
    query = "How many sub-sections in file operations section?"
    query = "Get me infomation on file operations in both C and Python"

    search_in_text(query, text_df)

    query = "Check if the image is a logo of a company"
    search_text_in_image(query, text_df, image_df)

    image_query_path = "documents/logo.jpeg"
    #TODO Need to fix below function 'search_image_by_image'
    # search_image_by_image(query, text_df, image_df, image_query_path)

    return True
  
  
if __name__ == "__main__":
    main()
