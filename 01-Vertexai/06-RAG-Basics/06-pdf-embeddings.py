import fitz
import numpy as np
from vertexai.language_models import TextEmbeddingModel

# Debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
logging.debug("Initialized TextEmbeddingModel")

def get_text_embedding_from_text_embedding_model(text):
    logging.debug(f"Entering get_text_embedding_from_text_embedding_model with text of length: {len(text)}")
    embeddings = text_embedding_model.get_embeddings([text])
    # logging.info(f"Obtained embeddings: {embeddings}")

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


def get_pdf_text(pdf_path):
    logging.debug(f"Entering get_pdf_text with pdf_path: {pdf_path}")
    pdf_text = ""

    with fitz.open(pdf_path) as pdf:
        logging.debug(f"Opened PDF file: {pdf_path}, total pages: {len(pdf)}")
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")
            logging.debug(f"Extracted text from page {page_number}: {page_text[:100]}... (truncated for brevity)")
            pdf_text += page_text

    logging.debug(f"Concatenated text length: {len(pdf_text)}")
    return pdf_text


def main():
    logging.debug("Main function started")
    pdf_file_path = "user_data/ramayan.pdf"  # Replace with your PDF file path

    text_bytes = get_pdf_text(pdf_file_path)
    logging.debug(f"Retrieved text from PDF of length: {len(text_bytes)}")

    embed_dict = get_embeddings_by_text(text_bytes)
    logging.debug(f"Generated embeddings dictionary with text length: {len(embed_dict['text'])} and embedding length: {len(embed_dict['text_embedding'])}")

    print(f"Text...\n{embed_dict['text'][:50]}... (truncated for brevity)")  # Display the first 500 characters
    print(f"Embeddings...\n{embed_dict['text_embedding'][:10]}... (truncated for brevity)")  # Display first 10 embedding values


if __name__ == "__main__":
    main()
