import chromadb
import logging
from embedding_utils import get_text_embedding_from_text_embedding_model

def get_or_create_vector_db(vdb_name, cname):
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)

    return collection    

def vdb_store_text_embeddings(vdb_collection):
    ids = ["1", "2", "3"]
    metadatas = [{"type": "system"}, {"type": "script"}, {"type": "script"}]
    documents = ["C Programming Language", "Java Script", "Python Scripting and Programming Language"]
    doc_embeddings = [get_text_embedding_from_text_embedding_model(doc, 5) for doc in documents]
    print(doc_embeddings)
    
    logging.debug(f"Upserting documents into the collection")
    logging.debug(f"IDs: {ids}")
    logging.debug(f"Metadata: {metadatas}")
    logging.debug(f"Documents: {documents}")
    logging.debug(f"embeddings: {doc_embeddings}")
    
    for i in range(len(ids)):
        vdb_collection.upsert(
            ids=ids[i],
            metadatas=metadatas[i],
            documents=documents[i],
            embeddings=doc_embeddings[i],
        )

    logging.info(f"Collection '{vdb_collection.name}' successfully updated.")
    return True

def main():
    vdb_name = "vectDB/progrmminVDB"
    coll_name = "programming"
    
    logging.debug(f"Starting main function.")
    logging.debug(f"Vector DB Path: {vdb_name}")
    logging.debug(f"Collection Name: {coll_name}")

    vdb = get_or_create_vector_db(vdb_name, coll_name)
    logging.debug(f"Success: VectorDB is created")

    vdb_store_text_embeddings(vdb)
    logging.info(f"Program completed successfully.")
    return True
  
if __name__ == "__main__":
    main()
