import pandas as pd
import json
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
    embeddings = text_embedding_model.get_embeddings([text])
    emb_values = [embedding.values for embedding in embeddings]
    text_embedding = emb_values[0]
    return text_embedding


def get_embeddings_by_text(text_data):
    embeddings_dict = {}
    if not text_data:
        return embeddings_dict
    text_embed = get_text_embedding_from_text_embedding_model(text=text_data)
    embeddings_dict["text"] = text_data
    embeddings_dict["text_embedding"] = text_embed
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
        full_text = ""
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")
            page_embed = get_embeddings_by_text(page_text)
            pdf_data["pages"].append({
                "page_number": page_number,
                "text": page_embed["text"],
                "embedding": page_embed["text_embedding"]
            })
            full_text += page_text

        pdf_data["file_text"]["text"] = full_text
        pdf_data["file_text"]["embedding"] = get_text_embedding_from_text_embedding_model(full_text)

        chunks = create_chunks_with_overlap(full_text)
        pdf_data["chunks"] = get_chunk_embed(chunks)

    return pdf_data


def save_to_dataframe_to_csv(pdf_data, csv_path):
    # Flatten the data into a DataFrame
    data = []

    # File-level text and embedding
    data.append({
        "level": "file",
        "text": pdf_data["file_text"]["text"],
        "embedding": pdf_data["file_text"]["embedding"]
    })

    # Page-level text and embedding
    for page in pdf_data["pages"]:
        data.append({
            "level": f"page_{page['page_number']}",
            "text": page["text"],
            "embedding": page["embedding"]
        })

    # Chunk-level text and embedding
    for chunk in pdf_data["chunks"]:
        data.append({
            "level": f"chunk_{chunk['chunk_id']}",
            "text": chunk["text"],
            "embedding": chunk["embedding"]
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to CSV and JSON
    df.to_csv(csv_path, index=False)
    logging.info(f"Data saved to {csv_path}")
    
    return df

def main():
    pdf_file_path = "user_data/cholas.pdf" 
    doc_embeddings = get_embeddings_by_page(pdf_file_path)

    pdf_embed_to_csv = pdf_file_path.split('.')[0].strip() + '.csv'
    
    df = save_to_dataframe_to_csv(doc_embeddings, pdf_embed_to_csv)
    logging.info("Process completed successfully.")
    print(df.head())


if __name__ == "__main__":
    main()
