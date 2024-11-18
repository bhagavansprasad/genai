import os
import glob
import json
import pandas as pd
import numpy as np
import fitz
import time

from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from vertexai.vision_models import Image as vision_model_Image

from vertexai.generative_models import GenerativeModel
from globals import GEN_AI_MODEL, multimodal_model, multimodal_embedding_model
from utils import get_text_embedding_from_text_embedding_model
from utils import smart_print_with_list_trimming

#Python funciton
def get_documents_list_to_rag(src_path):
    doc_list = []
    
    for pdf_path in glob.glob(src_path + "/*.pdf"):
        full_path = os.path.abspath(pdf_path)
        base_name = os.path.basename(full_path)
        
        doc_list.append({"doc_name" : base_name, "doc_path": full_path})

    return doc_list

def get_pdf_doc_object(pdf_path: str) -> tuple[fitz.Document, int]:
    print(pdf_path)
    doc: fitz.Document =  fitz.open(pdf_path)

    num_pages: int = len(doc)

    return doc, num_pages

def get_document_metadata(src_path):
    doc_list = get_documents_list_to_rag(src_path)
    
    for i, row in enumerate(doc_list):
        doc, page_count = get_pdf_doc_object(row["doc_path"])
        doc_list[i]["doc"] = doc
        doc_list[i]["page_count"] = page_count
    return doc_list

def get_page_text_embedding(text_data):
    embeddings_dict = {}

    print(f"text_data type :{type(text_data)}, len :{len(text_data)}")
    if not text_data:
        return embeddings_dict

    if isinstance(text_data, dict):
        for chunk_number, chunk_value in text_data.items():
            text_embed = get_text_embedding_from_text_embedding_model(text=chunk_value)
            embeddings_dict[chunk_number] = text_embed
    else:
        # Process the first 1000 characters of the page text
        text_embed = get_text_embedding_from_text_embedding_model(text=text_data)
        embeddings_dict["text_embedding"] = text_embed

    return embeddings_dict

def get_text_overlapping_chunk(text, character_limit = 1000, overlap = 100):
    if overlap > character_limit:
        raise ValueError("Overlap cannot be larger than character limit.")

    # Initialize variables
    chunk_number = 1
    chunked_text_dict = {}

    # Iterate over text with the given limit and overlap
    for i in range(0, len(text), character_limit - overlap):
        end_index = min(i + character_limit, len(text))
        chunk = text[i:end_index]

        # Encode and decode for consistent encoding
        chunked_text_dict[chunk_number] = chunk.encode("ascii", "ignore").decode(
            "utf-8", "ignore"
        )

        # Increment chunk number
        chunk_number += 1

    print(json.dumps(chunked_text_dict, indent=4))
    return chunked_text_dict

def text_embeddings_by_page(page, character_limit = 100, overlap = 10, embedding_size = 128):
    if overlap > character_limit:
        raise ValueError("Overlap cannot be larger than character limit.")

    # Extract text from the page
    text = page.get_text().encode("ascii", "ignore").decode("utf-8", "ignore")
    print(text)

    # Get whole-page text embeddings
    page_text_embeddings_dict = get_page_text_embedding(text)
    # print(f"embedding list :{page_text_embeddings_dict}")

    # Chunk the text with the given limit and overlap
    chunked_text_dict = get_text_overlapping_chunk(text, character_limit, overlap)
    # print(f"chunked_text_dict :{chunked_text_dict}")

    # Get embeddings for the chunks
    chunk_embeddings_dict: dict = get_page_text_embedding(chunked_text_dict)
    # print(f"chunk_embeddings_dict")
    # print(json.dumps(chunk_embeddings_dict, indent=4))

    return (text, page_text_embeddings_dict, chunked_text_dict, chunk_embeddings_dict)

def get_image_for_gemini(
    doc: fitz.Document,
    image: tuple,
    image_no: int,
    image_save_dir: str,
    file_name: str,
    page_num: int,
) -> Tuple[Image, str]:
    """
    Extracts an image from a PDF document, converts it to JPEG format (handling color conversions), saves it, and loads it as a PIL Image Object.
    """

    try:
        xref = image[0]
        pix = fitz.Pixmap(doc, xref)

        # Check and convert color space if needed
        if pix.colorspace not in (fitz.csGRAY, fitz.csRGB, fitz.csCMYK):
            pix = fitz.Pixmap(fitz.csRGB, pix)  # Convert to RGB

        # Now save as JPEG
        image_name = f"{image_save_dir}/{file_name}_image_{page_num}_{image_no}_{xref}.jpeg"
        os.makedirs(image_save_dir, exist_ok=True)
        pix.save(image_name)
        
        file_size = os.path.getsize(image_name)
        # Check if the file size is less than the minimum size
        if file_size < 3000:
            os.remove(image_name)
            return None, None
                
        image_for_gemini = Image.load_from_file(image_name)  # Use Image.open for loading
        return image_for_gemini, image_name

    except Exception as e:  # Catch-all for unexpected errors
        print(f"Unexpected error processing image: {e}")
        return None, None

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

image_description_prompt = """Explain what is going on in the image.
If it's a table, extract all elements of the table.
If it's a graph, explain the findings in the graph.
Do not include any numbers that are not mentioned in the image.
"""

generation_config: Optional[GenerationConfig] = GenerationConfig(temperature=0.2, max_output_tokens=2048)

def image_embeddings_by_page(doc, page_num, image, image_no, file_name, images_save_path):
    embedding_size: int = 128
    
    # for image_no, image in enumerate(images):
    image_number = int(image_no + 1)

    image_for_gemini, image_name = get_image_for_gemini(doc, image, image_no, images_save_path, file_name, page_num)

    if image_for_gemini is None:
        return None

    print(f"Extracting image from page: {page_num + 1}, saved as: {image_name}")

    # Generate image description using Gemini
    response = get_gemini_response(
        multimodal_model,
        model_input=[image_description_prompt, image_for_gemini],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
        
    image_embedding = get_image_embedding_from_multimodal_embedding_model(
        image_uri=image_name,
        embedding_size=embedding_size,
    )

    image_description_text_embedding = (
        get_text_embedding_from_text_embedding_model(text=response)
    )

    return (image_number, image_name, response, image_embedding, image_description_text_embedding)


def get_text_metadata_df(
    filename: str, text_metadata: Dict[Union[int, str], Dict]
) -> pd.DataFrame:
    """
    This function takes a filename and a text metadata dictionary as input,
    iterates over the text metadata dictionary and extracts the text, chunk text,
    and chunk embeddings for each page, creates a Pandas DataFrame with the
    extracted data, and returns it.

    Args:
        filename: The filename of the document.
        text_metadata: A dictionary containing the text metadata for each page.

    Returns:
        A Pandas DataFrame with the extracted text, chunk text, and chunk embeddings for each page.
    """

    final_data_text: List[Dict] = []

    for key, values in text_metadata.items():
        for chunk_number, chunk_text in values["chunked_text_dict"].items():
            data: Dict = {}
            data["file_name"] = filename
            data["page_num"] = int(key) + 1
            data["page_text"] = values["page_text"]
            data["text_embedding_page"] = values["page_text_embeddings"]["text_embedding"]
            data["chunk_number"] = chunk_number
            data["chunk_text"] = chunk_text
            data["text_embedding_chunk"] = values["chunk_embeddings_dict"][chunk_number]

            final_data_text.append(data)

    return_df = pd.DataFrame(final_data_text)
    return_df = return_df.reset_index(drop=True)
    return return_df
    
def get_image_metadata_df(
    filename: str, image_metadata: Dict[Union[int, str], Dict]
) -> pd.DataFrame:
    """
    This function takes a filename and an image metadata dictionary as input,
    iterates over the image metadata dictionary and extracts the image path,
    image description, and image embeddings for each image, creates a Pandas
    DataFrame with the extracted data, and returns it.

    Args:
        filename: The filename of the document.
        image_metadata: A dictionary containing the image metadata for each page.

    Returns:
        A Pandas DataFrame with the extracted image path, image description, and image embeddings for each image.
    """

    final_data_image: List[Dict] = []
    for key, values in image_metadata.items():
        for _, image_values in values.items():
            data: Dict = {}
            data["file_name"] = filename
            data["page_num"] = int(key) + 1
            data["img_num"] = int(image_values["img_num"])
            data["img_path"] = image_values["img_path"]
            data["img_desc"] = image_values["img_desc"]
            # data["mm_embedding_from_text_desc_and_img"] = image_values[
            #     "mm_embedding_from_text_desc_and_img"
            # ]
            data["mm_embedding_from_img_only"] = image_values[
                "mm_embedding_from_img_only"
            ]
            data["text_embedding_from_image_description"] = image_values[
                "text_embedding_from_image_description"
            ]
            final_data_image.append(data)

    return_df = pd.DataFrame(final_data_image).dropna()
    return_df = return_df.reset_index(drop=True)
    return return_df

def process_document(document, images_save_path, add_sleep_after_page: bool = False, sleep_time_after_page: int = 2):
    file_name = document["doc_name"]
    doc = document["doc"]
    pcount = document["page_count"]
    text_metadata: Dict[Union[int, str], Dict] = {}
    image_metadata: Dict[Union[int, str], Dict] = {}
   
    for page_num, page in enumerate(doc):
        retval = text_embeddings_by_page(page)
        text, page_text_embedding_dict, chunk_text_dict, chunk_embeddings_dict = retval
        text_metadata[page_num] = {
            "page_text": text,
            "page_text_embeddings": page_text_embedding_dict,
            "chunked_text_dict": chunk_text_dict,
            "chunk_embeddings_dict": chunk_embeddings_dict
        }
        smart_print_with_list_trimming(text_metadata, max_item_length=500, max_list_items=5)

        images = page.get_images()
        image_metadata[page_num] = {}
        for image_no, image in enumerate(images):
            retval = image_embeddings_by_page(doc, page_num, image, image_no, file_name, images_save_path)
            if (retval == None):
                continue
            image_number, image_name, response, image_embedding, image_description_text_embedding = retval

            image_metadata[page_num][image_number] = {}
            image_metadata[page_num][image_number] = {
                "img_num": image_number,
                "img_path": image_name,
                "img_desc": response,
                # "mm_embedding_from_text_desc_and_img": image_embedding_with_description,
                "mm_embedding_from_img_only": image_embedding,
                "text_embedding_from_image_description": image_description_text_embedding,
            }
            # Add sleep to reduce issues with Quota error on API
            if add_sleep_after_page:
                time.sleep(sleep_time_after_page)
                print(
                    "Sleeping for ",
                    sleep_time_after_page,
                    """ sec before processing the next page to avoid quota issues. You can disable it: "add_sleep_after_page = False"  """,
                )

        smart_print_with_list_trimming(image_metadata, max_item_length=500, max_list_items=5)

    print("+"*50)
    smart_print_with_list_trimming(text_metadata, max_item_length=500, max_list_items=5)
    print("-"*50)
    smart_print_with_list_trimming(image_metadata, max_item_length=500, max_list_items=5)
    print("+"*50)

    text_metadata_df = get_text_metadata_df(file_name, text_metadata)
    image_metadata_df = get_image_metadata_df(file_name, image_metadata)

    print(image_metadata_df.columns)
    
    return text_metadata_df, image_metadata_df

def process_documents_data(doc_list, images_save_path):
    text_metadata_df_final, image_metadata_df_final = pd.DataFrame(), pd.DataFrame()
    for i, row in enumerate(doc_list):
        text_metadata_df, image_metadata_df = process_document(row, images_save_path, True, 10)
        
        text_metadata_df_final = pd.concat([text_metadata_df_final, text_metadata_df], axis=0)
        image_metadata_df_final = pd.concat([image_metadata_df_final, image_metadata_df.drop_duplicates(subset=["img_desc"])], axis=0)

    text_metadata_df_final = text_metadata_df_final.reset_index(drop=True)
    image_metadata_df_final = image_metadata_df_final.reset_index(drop=True)
    
    return text_metadata_df_final, image_metadata_df_final

def dump_doc_list(doc_list):
    for i, row in enumerate(doc_list):
        print        
        print(f"{i}:", end=" ")
        print(f"Name    :{row['doc_name']}")
        print(f"Path       :{row['doc_path']}")
        print(f"Page count :{row['page_count']}")
        print()

def docs_to_embeddings_to_csv_n_json(text_embeddings_csv, image_embeddings_csv):
    image_description_prompt = """Explain what is going on in the image.
    If it's a table, extract all elements of the table.
    If it's a graph, explain the findings in the graph.
    Do not include any numbers that are not mentioned in the image.
    """
    multimodal_model = GenerativeModel(GEN_AI_MODEL)
    text_metadata_df_final, image_metadata_df_final = pd.DataFrame(), pd.DataFrame()
    images_save_path = "./documents/images"

    doc_list = get_document_metadata("./documents")
    dump_doc_list(doc_list)
    
    docs_text_metadata, docs_image_metadata = process_documents_data(doc_list, images_save_path)
    docs_text_metadata.to_csv(text_embeddings_csv)
    docs_image_metadata.to_csv(image_embeddings_csv)
    
    docs_text_metadata.to_json('rag_data/docs_text.json')
    docs_image_metadata.to_json('rag_data/docs_image.json')

    
def main():
    text_embeddings_csv = 'rag_data/docs_text.csv'
    image_embeddings_csv = 'rag_data/docs_image.csv'
    docs_to_embeddings_to_csv_n_json(text_embeddings_csv, image_embeddings_csv)
    return True
  
  
if __name__ == "__main__":
    main()
