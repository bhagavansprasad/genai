import logging
import fitz
from vertexai.language_models import TextEmbeddingModel

def create_chunks_with_overlap(text, page_number=0, chunk_size=256, overlap=32):
    chunks = []
    text_bytes = text.encode('utf-8')
    i = 0
    for i in range(0, len(text_bytes) - chunk_size + 1, chunk_size - overlap):
        chunks.append(text_bytes[i:i + chunk_size].strip())
        
    if (i == 0):
        chunks.append(text_bytes)
    else:
        chunks.append(text_bytes[i+chunk_size:].strip())
    
    return [chunk.decode('utf-8', errors='ignore') for chunk in chunks]

def get_pdf_text_chunks(pdf_path, page_number=0, chunk_size=10, overlap=3):
    text_bytes = get_pdf_text(pdf_path)
    
    print(f"File content, len :{len(text_bytes)}")
    
    return create_chunks_with_overlap(text_bytes, page_number=page_number, chunk_size=chunk_size, overlap=overlap)

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


def get_pdf_page_embeddings(pdf_path):
    logging.debug(f"Entering get_pdf_text with pdf_path: {pdf_path}")
    pdf_text = ""
    pages_embed = []

    with fitz.open(pdf_path) as pdf:
        logging.debug(f"Opened PDF file: {pdf_path}, total pages: {len(pdf)}")
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")
            logging.debug(f"Extracted text from page {page_number}: {page_text[:100]}... (truncated for brevity)")
            
            page_embed = get_embeddings_by_text(page_text)
            page_embed['page_number'] = page_number
            pages_embed.append(page_embed)
            
            pdf_text += page_text

    logging.debug(f"Concatenated text length: {len(pdf_text)}")
    return pages_embed, pdf_text

def get_text_embedding_from_text_embedding_model(text, output_dimensionality=None):
    logging.debug(f"Entering get_text_embedding_from_text_embedding_model with text of length: {len(text)}")
    
    text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=output_dimensionality)

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

def get_text_embedding(text, output_dimensionality=None):
    logging.debug(f"Generating embeddings for text of length: {len(text)}")
    text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=output_dimensionality)
    embedding_values = embeddings[0].values
    logging.debug(f"Generated embedding with first 5 values: {embedding_values[:5]}")
    return embedding_values


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

def get_pdf_embeddings(pdf_path):
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
            page_text = page.get_text("text")
            logging.debug(f"Extracted text from page {page_number}: {page_text[:100]}... (truncated for brevity)")

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

    logging.debug("Completed processing PDF file.")
    return pdf_data
