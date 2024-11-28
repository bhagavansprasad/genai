import chromadb
import logging
from embedding_utils import get_pdf_embeddings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_vector_db(vdb_name, cname):
    logging.debug(f"Initializing ChromaDB PersistentClient with path: {vdb_name}")
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)
    return collection

def store_embeddings_in_vectordb(collection, page_embeddings):
    logging.debug("Storing page embeddings into ChromaDB")
    print(page_embeddings)
    print(type(page_embeddings))
    exit(1)
    for page in page_embeddings:
        print(page.keys())
        exit(1)
        collection.upsert(
            documents=[page["text"]],
            metadatas=[{"page_number": page["page_number"]}],
            ids=[f"page-{page['page_number']}"],
            embeddings=[page["embedding"]]
        )
    logging.info(f"Collection '{collection.name}' successfully updated.")

def main():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"
    pdf_path = "user_data/cholas.pdf"

    collection = initialize_vector_db(vdb_name, coll_name)

    page_embeddings = get_pdf_embeddings(pdf_path)

    store_embeddings_in_vectordb(collection, page_embeddings)
    logging.info("Process completed successfully!")
    
    print(collection.get())
    result = collection.get(ids=["page-1"], include=["documents", "metadatas", "embeddings"])
    result = collection.get(include=["documents", "metadatas", "embeddings"])
    print(result)
    
if __name__ == "__main__":
    main()
