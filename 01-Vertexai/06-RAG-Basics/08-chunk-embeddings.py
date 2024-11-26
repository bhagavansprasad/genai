import fitz
import numpy as np
from pprint import pprint
from vertexai.language_models import TextEmbeddingModel

# Debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
logging.debug("Initialized TextEmbeddingModel")

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

def get_text_embedding_from_text_embedding_model(text):
    logging.debug(f"Entering get_text_embedding_from_text_embedding_model with text of length: {len(text)}")
    embeddings = text_embedding_model.get_embeddings([text])
    emb_values = [embedding.values for embedding in embeddings]
    text_embedding = emb_values[0]
    logging.debug(f"Extracted embedding values: {text_embedding[:10]}... (truncated for brevity)")

    return text_embedding


def get_embeddings_by_text(text_data):
    logging.debug(f"Entering get_embeddings_by_text with text_data of length: {len(text_data)}")
    embeddings_dict = {}

    if not text_data:
        logging.debug("Empty text_data provided; returning empty embeddings_dict")
        return embeddings_dict

    text_embed = get_text_embedding_from_text_embedding_model(text=text_data)
    embeddings_dict["text"] = text_data
    embeddings_dict["text_embedding"] = text_embed
    logging.debug(f"Generated embeddings_dict with keys: {list(embeddings_dict.keys())}")

    return embeddings_dict


def create_chunks_with_overlap(text, page_number=0, chunk_size=256, overlap=32):
    chunks = []
    text_bytes = text.encode('utf-8')
    for i in range(0, len(text_bytes) - chunk_size + 1, chunk_size - overlap):
        chunks.append(text_bytes[i:i + chunk_size].strip())
    return [chunk.decode('utf-8', errors='ignore') for chunk in chunks]


def get_chunk_embed(chunks):
    chunk_embeds = []
    for chunk_id, chunk in enumerate(chunks, 1):
        chunk_embed = get_embeddings_by_text(chunk)
        chunk_embeds.append({
            "chunk_id": chunk_id,
            "text": chunk,
            "embedding": chunk_embed["text_embedding"]
        })
    return chunk_embeds


def get_embeddings_by_page(pdf_path):
    logging.debug(f"Entering get_pdf_text with pdf_path: {pdf_path}")
    pdf_data = {
        "file_name": pdf_path.split("/")[-1],
        "file_text": {
            "text": "",
            "embedding": []
        },
        "pages": [],
        "chunks": []
    }

    with fitz.open(pdf_path) as pdf:
        logging.debug(f"Opened PDF file: {pdf_path}, total pages: {len(pdf)}")
        full_text = ""

        for page_number, page in enumerate(pdf, start=1):
            # Extract text from page
            page_text = page.get_text("text")
            logging.debug(f"Extracted text from page {page_number}: {page_text[:100]}... (truncated for brevity)")

            # Generate embeddings for the page
            page_embed = get_embeddings_by_text(page_text)
            pdf_data["pages"].append({
                "page_number": page_number,
                "text": page_embed["text"],
                "embedding": page_embed["text_embedding"]
            })

            # Append page text to full_text
            full_text += page_text

        # Generate embeddings for the full text
        pdf_data["file_text"]["text"] = full_text
        pdf_data["file_text"]["embedding"] = get_text_embedding_from_text_embedding_model(full_text)

        # Create chunks and their embeddings
        chunks = create_chunks_with_overlap(full_text)
        pdf_data["chunks"] = get_chunk_embed(chunks)

    logging.debug("Completed processing PDF file.")
    return pdf_data

def main():
    file_obj_embed = []
    logging.debug("Main function started")
    pdf_file_path = "user_data/cholas.pdf" 
    
    doc_embeddings = get_embeddings_by_page(pdf_file_path)
    smart_print_with_list_trimming(doc_embeddings)
    
if __name__ == "__main__":
    main()

