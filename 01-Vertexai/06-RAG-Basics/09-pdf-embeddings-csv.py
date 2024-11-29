import pandas as pd
import json
import fitz
import numpy as np
from pprint import pprint
from vertexai.language_models import TextEmbeddingModel
from embeddings_utils import get_pdf_embeddings

import logging
logging.basicConfig(level=logging.DEBUG)

def save_to_dataframe_to_csv(pdf_data, csv_path):
    df = pd.DataFrame([pdf_data])

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
