import pandas as pd
from embeddings_utils import get_pdf_embeddings

# Debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

def save_to_dataframe_to_json(pdf_data, json_path):
    df = pd.DataFrame([pdf_data])

    df.to_json(json_path, orient="records", indent=4)

    logging.info(f"Data saved to {json_path}")
    return df

def main():
    pdf_file_path = "user_data/cholas.pdf" 
    json_embd_path = "embeddings/cholas.json" 
    doc_embeddings = get_pdf_embeddings(pdf_file_path)

    df = save_to_dataframe_to_json(doc_embeddings, json_embd_path)
    logging.info("Process completed successfully.")

    print(df.head())

if __name__ == "__main__":
    main()
