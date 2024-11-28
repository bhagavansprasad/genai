import chromadb
import logging
from vertexai.language_models import TextEmbeddingModel

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Initialized TextEmbeddingModel")

def get_text_embedding(text, output_dimensionality=None):
    logging.debug(f"Generating embeddings for text of length: {len(text)}")
    embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=output_dimensionality)
    embedding_values = embeddings[0].values
    logging.debug(f"Generated embedding with first 5 values: {embedding_values[:5]}")
    return embedding_values

def get_or_create_vector_db(vdb_name, cname):
    logging.debug(f"Initializing ChromaDB PersistentClient with path: {vdb_name}")
    client = chromadb.PersistentClient(path=vdb_name)

    logging.debug(f"Fetching or creating collection with name: {cname}")
    collection = client.get_or_create_collection(name=cname)

    return collection    

def vdb_search_by_query(collection, id_value=None):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

def main():
    vdb_name = "vectDB/progrmminVDB"
    coll_name = "programming"
    
    vdb = get_or_create_vector_db(vdb_name, coll_name)
    logging.debug(f"Success: VectorDB is created")

    query_text = "Programming Language"
    query_embedding = get_text_embedding(query_text, 5)
    retval = vdb.query(query_embeddings=[query_embedding], n_results=2)

    print(retval)
    return True
  
if __name__ == "__main__":
    main()
