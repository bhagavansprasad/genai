import pandas as pd
import json
import fitz
import numpy as np
from pprint import pprint
from vertexai.language_models import TextEmbeddingModel
from embedding_utils import get_pdf_embeddings

# Debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

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
    csv_embd_path = "embeddings/cholas.csv" 
    doc_embeddings = get_pdf_embeddings(pdf_file_path)

    df = save_to_dataframe_to_csv(doc_embeddings, csv_embd_path)
    logging.info("Process completed successfully.")
    print(df.head())


if __name__ == "__main__":
    main()
