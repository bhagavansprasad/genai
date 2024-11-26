import fitz
import chromadb
import logging
from vertexai.language_models import TextEmbeddingModel
from chromadb.config import Settings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def initialize_vector_db(vdb_name, cname):
    logging.debug(f"Initializing ChromaDB PersistentClient with path: {vdb_name}")
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)
    return collection

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
logging.debug("Initialized TextEmbeddingModel")

def get_text_embedding(text):
    logging.debug(f"Generating embeddings for text of length: {len(text)}")
    embeddings = text_embedding_model.get_embeddings([text])
    embedding_values = embeddings[0].values
    logging.debug(f"Generated embedding with first 5 values: {embedding_values[:5]}")
    return embedding_values

def get_pdf_page_embeddings(pdf_path):
    logging.debug(f"Processing PDF: {pdf_path}")
    page_embeddings = []

    with fitz.open(pdf_path) as pdf:
        logging.debug(f"Opened PDF with {len(pdf)} pages")
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")
            logging.debug(f"Extracted text from page {page_number}: {page_text[:100]}... (truncated)")
            
            embedding = get_text_embedding(page_text)
            page_embeddings.append({
                "page_number": page_number,
                "text": page_text,
                "embedding": embedding
            })

    return page_embeddings

def store_embeddings_in_vectordb(collection, page_embeddings):
    logging.debug("Storing page embeddings into ChromaDB")
    for page in page_embeddings:
        collection.upsert(
            documents=[page["text"]],
            metadatas=[{"page_number": page["page_number"]}],
            ids=[f"page-{page['page_number']}"],
            embeddings=[page["embedding"]]
        )
    logging.info("Successfully stored page embeddings in ChromaDB")

def main():
    vdb_name = "user_data/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"
    pdf_path = "user_data/cholas.pdf"

    collection = initialize_vector_db(vdb_name, coll_name)

    page_embeddings = get_pdf_page_embeddings(pdf_path)

    store_embeddings_in_vectordb(collection, page_embeddings)

    logging.info("Process completed successfully!")
    
    print(collection.get())
    result = collection.get(ids=["page-1"], include=["documents", "metadatas", "embeddings"])
    result = collection.get(include=["documents", "metadatas", "embeddings"])
    print(result)
    
if __name__ == "__main__":
    main()
