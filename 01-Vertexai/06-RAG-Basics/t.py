import chromadb
import numpy as np

from vertexai.language_models import TextEmbeddingModel

text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

def get_or_create_vector_db(vdb_name, cname):
    client = chromadb.PersistentClient(path=vdb_name)
    collection = client.get_or_create_collection(name=cname)

    return collection    

def get_text_embedding(text, output_dimensionality=None):
    embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=output_dimensionality)
    embedding_values = embeddings[0].values
    return embedding_values

def vdb_search_text_vectorDB(collection, id_value):
    results = collection.get(ids=[id_value], include=["documents", "metadatas", "embeddings"])
    return results

# Example text data
text_data = [
    "ChromaDB is an open-source vector database.",
    "Embeddings can be used for search, recommendation, and clustering.",
    "Chroma stores vectors in a highly efficient way."
]

# Generate embeddings for each string
embeddings = [get_text_embedding(text) for text in text_data]

vdb_name = "vectDB/sample"
coll_name = "sample"
vdb = get_or_create_vector_db(vdb_name, coll_name)
# Insert strings and embeddings into ChromaDB
for i, text in enumerate(text_data):
    vdb.add(
        documents=[text],  # Text data
        metadatas=[{"source": f"source_{i}"}],  # Optional metadata
        embeddings=[embeddings[i]],  # Embeddings
        ids=[str(i)]  # Unique ID for each document
    )

# Querying the collection with a new text to find similar embeddings
query_text = "Tell me about vector databases."
query_embedding = get_text_embedding(query_text)

# Retrieve the most similar document
results = vdb.query(
    query_embeddings=[query_embedding],
    n_results=1
)

print("Most similar document:", results['documents'][0])

retval = vdb_search_text_vectorDB(vdb, "1")
print(retval)

