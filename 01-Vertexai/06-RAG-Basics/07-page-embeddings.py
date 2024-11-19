import fitz
import numpy as np
from vertexai.language_models import TextEmbeddingModel

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

def get_text_embedding_from_text_embedding_model(text, return_array = False):
    embeddings = text_embedding_model.get_embeddings([text])

    emb_len = len(embeddings)
    emb_values = [embedding.values for embedding in embeddings]
    text_embedding = emb_values[0]              # Debug [0]

    if return_array:
        text_embedding = np.fromiter(text_embedding, dtype=float)

    # returns 768 dimensional array
    return text_embedding


def get_page_text_embedding(text_data):
    embeddings_dict = {}

    print(f"text_data type :{type(text_data)}, len :{len(text_data)}")
    if not text_data:
        return embeddings_dict

    text_embed = get_text_embedding_from_text_embedding_model(text=text_data)
    embeddings_dict["text_embedding"] = text_embed

    return embeddings_dict


def text_embeddings_by_page(text):
    page_text_embeddings_dict = get_page_text_embedding(text)
    return (page_text_embeddings_dict)

def create_chunks_with_overlap(pdf_path, page_number=0, chunk_size=10, overlap=3):
    chunks = []
    
    with fitz.open(pdf_path) as pdf:
        if page_number >= len(pdf):
            raise ValueError("Page number exceeds the number of pages in the PDF.")
        
        page = pdf[page_number]
        text = page.get_text("text")  # Extract text from the page
    
    text_bytes = text.encode('utf-8')
    
    text_embeddings_by_page(text_bytes)
    for i in range(0, len(text_bytes) - chunk_size + 1, chunk_size - overlap):
        chunks.append(text_bytes[i:i + chunk_size].strip())
    
    return [chunk.decode('utf-8', errors='ignore') for chunk in chunks]

# Example usage
if __name__ == "__main__":
    print("YET TO IMPLIMENT THIS FUNCTIONALITY")
    exit(1)
    pdf_file_path = "ramayan.pdf"  # Replace with your PDF file path
    chunks = create_chunks_with_overlap(pdf_file_path, page_number=0, chunk_size=30, overlap=5)
    
    print(f"Total Chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk}")

