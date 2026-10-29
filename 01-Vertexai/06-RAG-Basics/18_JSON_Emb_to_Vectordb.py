import pandas as pd
import chromadb
import logging
from chromadb_utils import get_or_create_vector_db
from chromadb_utils import pdf_store_embeddings_in_vectordb
from vertexai.language_models import TextEmbeddingModel

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
logging.debug("Initialized TextEmbeddingModel")

    
def load_embeddings_from_json(csv_embeddings):
    dataframe  = pd.read_json(csv_embeddings)
    return dataframe

def main():
    print("NOT IMPLIMENTED...ITS A BUGGY CODE")
    exit(1)
    csv_embeddings_path = 'embeddings/cholas.json'
    vdb_name = "vectDB/pdf-vectorDB"
    coll_name = "pdf-page-embeddings"
 
    text_df = load_embeddings_from_json(csv_embeddings_path)
    print(text_df.head()) 
    print(text_df.columns)
    
    data = text_df.to_dict()
    collection = get_or_create_vector_db(vdb_name, coll_name)
    pdf_store_embeddings_in_vectordb(collection, data)
    return True
  
if __name__ == "__main__":
    main()
