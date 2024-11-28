import chromadb
import logging
from pprint import pprint
from vertexai.language_models import TextEmbeddingModel

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
logging.debug("Initialized TextEmbeddingModel")

def smart_print_with_list_trimming(dictionary, max_item_length=20, max_list_items=5):
    def trim_value(value):
        if isinstance(value, dict):  # Handle nested dictionaries
            return {k: trim_value(v) for k, v in value.items()}
        elif isinstance(value, list):  # Trim list items and limit list length
            return [trim_value(v) for v in value[:max_list_items]]
        elif isinstance(value, str) and len(value) > max_item_length:  # Trim long strings
            return value[:max_item_length] + "..."
        else:
            return value

    trimmed_dict = {k: trim_value(v) for k, v in dictionary.items()}
    pprint(trimmed_dict)
    print()

def initialize_vector_db(vdb_name, cname):
    logging.debug(f"Initializing ChromaDB PersistentClient with path: {vdb_name}")
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)
    return collection

def read_page_collection(collection, id_value):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

def main():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"

    collection = initialize_vector_db(vdb_name, coll_name)

    
    id_value = "page-1"
    print(f"Search ChromaDB content id :{id_value}...")
    retval = read_page_collection(collection, id_value)
    smart_print_with_list_trimming(retval)

    id_value = "chunk_1"
    retval = read_page_collection(collection, id_value)
    smart_print_with_list_trimming(retval)


    return
    
if __name__ == "__main__":
    main()
