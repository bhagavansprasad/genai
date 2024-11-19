import fitz
import numpy as np
from vertexai.language_models import TextEmbeddingModel

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

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


def get_pdf_text(pdf_path):
    chunks = []

    pdf_text = ""
        
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            pdf_text += page.get_text("text")  # Extract text from the page
    
    return pdf_text

def main():
    pdf_file_path = "ramayan.pdf"  # Replace with your PDF file path

    text_bytes = get_pdf_text(pdf_file_path)
    
    embed_dict = get_embeddings_by_text(text_bytes)
    print(f"Text...\n{embed_dict['text']}")
    print(f"Embeddings...\n{embed_dict['text_embedding']}")
    
    print()

if __name__ == "__main__":
    main()
    

