import logging
from chromadb_utils import initialize_vector_db

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def read_page_collection(collection, id_value):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

def main():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"

    collection = initialize_vector_db(vdb_name, coll_name)

    return
    
if __name__ == "__main__":
    main()
