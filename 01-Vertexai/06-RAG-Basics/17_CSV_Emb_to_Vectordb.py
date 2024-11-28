import pandas as pd
import chromadb
import logging
from vertexai.language_models import TextEmbeddingModel

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
logging.debug("Initialized TextEmbeddingModel")


def initialize_vector_db(vdb_name, cname):
    logging.debug(f"Initializing ChromaDB PersistentClient with path: {vdb_name}")
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)
    return collection

def store_embeddings_in_vectordb(collection, data):
    logging.debug("Storing page embeddings into ChromaDB")

    ids = [data['level'][e] for e in data['level']]
    documents = [data['text'][e] for e in data['text']]
    metadata = [{"key": key, "value": value} for key, value in data['level'].items()]
    embeddings = [data['embedding'][e] for e in data['embedding']]

    logging.info(f"len ids        :{len(ids)}")
    logging.info(f"len documents  :{len(documents)}")
    logging.info(f"len metadata   :{len(metadata)}")
    logging.info(f"len embeddings :{len(embeddings)}")

    collection.upsert(ids=ids, documents=documents, metadatas=metadata, embeddings=embeddings)
    logging.info(f"Collection '{collection.name}' successfully updated.")
    return
    
def load_embeddings_from_csv(csv_embeddings):
    dataframe  = pd.read_csv(csv_embeddings)
    return dataframe

def main():
    csv_embeddings_path = 'embeddings/cholas.csv'
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"
 
    text_df = load_embeddings_from_csv(csv_embeddings_path)
    print(text_df.head()) 
    print(text_df.columns)
    
    data = text_df.to_dict()
    collection = initialize_vector_db(vdb_name, coll_name)
    store_embeddings_in_vectordb(collection, data)
    return True
  
if __name__ == "__main__":
    main()
