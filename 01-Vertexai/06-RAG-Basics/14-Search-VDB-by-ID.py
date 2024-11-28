import chromadb
import logging
from vertexai.language_models import TextEmbeddingModel

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")


def get_or_create_vector_db(vdb_name, cname):
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)

    return collection    

def vdb_search_by_id(collection, id_value=None):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

def vdb_search_by_query(collection, id_value=None):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

def main():
    vdb_name = "vectDB/progrmminVDB"
    coll_name = "programming"
    
    vdb = get_or_create_vector_db(vdb_name, coll_name)

    retval = vdb_search_by_id(vdb, "1")
    print(retval)
    return True
  
if __name__ == "__main__":
    main()
