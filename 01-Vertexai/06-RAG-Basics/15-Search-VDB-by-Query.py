import logging
from chromadb_utils import get_or_create_vector_db
from chromadb_utils import vdb_search_by_query

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    vdb_name = "vectDB/progrmminVDB"
    coll_name = "programming"
    
    collection = get_or_create_vector_db(vdb_name, coll_name)
    logging.debug(f"Success: VectorDB is created")

    query_text = "Programming Language"
    retval = vdb_search_by_query(collection, query_text)
    
    print(retval)
    return True
  
if __name__ == "__main__":
    main()
