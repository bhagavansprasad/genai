import logging
from dump_utils import smart_print_with_list_trimming
from chromadb_utils import get_or_create_vector_db

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def read_collection_by_name(collection):
    results = collection.get()
    return results

def read_page_collection(collection, id_value):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

def read_selected_sections_02(collection):
    results = collection.get(include=["documents"])
    return results

def main():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"

    collection = get_or_create_vector_db(vdb_name, coll_name)

    print("Dumping ChromaDB content...")
    retval = read_collection_by_name(collection)
    smart_print_with_list_trimming(retval)
    
    id_value = "page-id-1"
    print(f"Search ChromaDB content id :{id_value}...")
    retval = read_page_collection(collection, id_value)
    smart_print_with_list_trimming(retval)

    id_value = "chunk-id-1"
    retval = read_page_collection(collection, id_value)
    smart_print_with_list_trimming(retval)

    print("Dumping ChromaDB ONLY document list...")
    retval = read_selected_sections_02(collection)
    smart_print_with_list_trimming(retval)

    return
    
if __name__ == "__main__":
    main()
