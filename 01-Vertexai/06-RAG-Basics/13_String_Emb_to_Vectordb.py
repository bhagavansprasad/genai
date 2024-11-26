import chromadb
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_or_create_vector_db(vdb_name, cname):
    logging.debug(f"Initializing ChromaDB PersistentClient with path: {vdb_name}")
    client = chromadb.PersistentClient(path=vdb_name)

    logging.debug(f"Fetching or creating collection with name: {cname}")
    collection = client.get_or_create_collection(name=cname)
    
    documents = ["C Programming Language", "Java Script", "Python Scripting and Programming Language"]
    metadatas = [{"type": "system"}, {"type": "script"}, {"type": "script"}]
    ids = ["1", "2", "3"]
    
    logging.debug(f"Upserting documents into the collection")
    logging.debug(f"Documents: {documents}")
    logging.debug(f"Metadata: {metadatas}")
    logging.debug(f"IDs: {ids}")
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    logging.info(f"Collection '{cname}' successfully updated.")
    return True

def main():
    vdb_name = "user_data/aura-vectorDB"
    coll_name = "programming-coll"
    
    logging.debug(f"Starting main function.")
    logging.debug(f"Vector DB Path: {vdb_name}")
    logging.debug(f"Collection Name: {coll_name}")

    result = get_or_create_vector_db(vdb_name, coll_name)
    logging.debug(f"Result from get_or_create_vector_db: {result}")
    
    logging.info(f"Program completed successfully.")
    return True
  
if __name__ == "__main__":
    main()
