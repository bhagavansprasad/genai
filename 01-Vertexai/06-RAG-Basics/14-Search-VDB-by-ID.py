from chromadb_utils import get_or_create_vector_db
from chromadb_utils import vdb_search_by_id

def main():
    vdb_name = "vectDB/progrmminVDB"
    coll_name = "programming"
    
    vdb = get_or_create_vector_db(vdb_name, coll_name)

    retval = vdb_search_by_id(vdb, "1")
    print(retval)
    return True
  
if __name__ == "__main__":
    main()
