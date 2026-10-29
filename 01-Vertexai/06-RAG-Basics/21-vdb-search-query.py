from chromadb_utils import get_or_create_vector_db
from chromadb_utils import vdb_search_by_query
from chromadb_utils import vdb_search_by_query_ids

def read_collection_by_name(collection):
    results = collection.get()
    return results

def read_page_collection(collection, id_value):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

def read_selected_sections_02(collection):
    results = collection.get(include=["documents"])
    return results

def print_results(s1, s2, s3):
    print(s1, s2, s3)
    
def dump_search_results(query_results):
    ids = query_results['ids'][0]
    docs = query_results['documents'][0]
    distances = query_results['distances'][0]
    
    for i, (id, doc, distance) in enumerate(zip(ids, docs, distances), 1):
        print(f"{i}. ID: {id}")
        print(f"doc :{doc}")
        print(f"distance :{distance}")
        print()
    return 0

# points to note
# Query is valid only when the search query-embedding and stored-chunk-embedding dimentions is same

def search_query_01():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "ramayan-embeddings"

    collection = get_or_create_vector_db(vdb_name, coll_name)
    
    query_text = "Who is the Author of Ramayan"
    retval = vdb_search_by_query(collection, query_text, n_results=5)
    dump_search_results(retval)

def search_query_02():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "cholas-embeddings"

    collection = get_or_create_vector_db(vdb_name, coll_name)
    
    query_text = "When the chola dynasty started?"
    retval = vdb_search_by_query(collection, query_text, n_results=5)
    dump_search_results(retval)

def search_query_03():
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "cholas-embeddings"

    collection = get_or_create_vector_db(vdb_name, coll_name)
    
    query_text = "When the chola dynasty started?"
    
    retval = vdb_search_by_query_ids(collection=collection, query_text=query_text, only_chunks=True)
    dump_search_results(retval)
    
def main():
    search_query_01()
    search_query_02()
    search_query_03()
    
    return True
  
if __name__ == "__main__":
    main()
