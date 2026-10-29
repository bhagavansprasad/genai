import logging
from chromadb_utils import get_or_create_vector_db
from chromadb_utils import vectordb_store_page_embeddings, store_embeddings_in_vectordb
from chromadb_utils import pdf_store_embeddings_in_vectordb
from embeddings_utils import get_pdf_embeddings

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    vdb_name = "vectDB/pdf-vectorDB"

    coll_name = "cholas-embeddings"
    pdf_path = "user_data/cholas.pdf"

    # coll_name = "ramayan-embeddings"
    # pdf_path = "user_data/ramayan.pdf"

    collection = get_or_create_vector_db(vdb_name, coll_name)

    page_embeddings = get_pdf_embeddings(pdf_path)

    pdf_store_embeddings_in_vectordb(collection, page_embeddings)
    logging.info("Process completed successfully!")
    
    # print(collection.get())
    # result = collection.get(ids=["page-1"], include=["documents", "metadatas", "embeddings"])
    # result = collection.get(include=["documents", "metadatas", "embeddings"])
    # print(result)
    
if __name__ == "__main__":
    main()
