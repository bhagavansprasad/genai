import chromadb
import logging
from vertexai.language_models import TextEmbeddingModel

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
logging.debug("Initialized TextEmbeddingModel")

def initialize_vector_db(vdb_name, cname):
    logging.debug(f"Initializing ChromaDB PersistentClient with path: {vdb_name}")
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)
    return collection

def read_collection_by_name(collection):
    result = collection.get()
    print(result)

def read_page_collection(collection, page_name):
    result = collection.get(ids=[page_name], include=["documents", "metadatas", "embeddings"])
    print(result)

def read_selected_sections_01(collection):
    result = collection.get(include=["documents", "metadatas", "embeddings"])
    print(result)
    print()

def read_selected_sections_02(collection):
    result = collection.get(include=["documents"])
    print(result)
    print()

def main():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"

    collection = initialize_vector_db(vdb_name, coll_name)

    read_collection_by_name(collection)
    read_page_collection(collection, "page-1")
    read_selected_sections_01(collection)
    read_selected_sections_02(collection)
    
if __name__ == "__main__":
    main()
