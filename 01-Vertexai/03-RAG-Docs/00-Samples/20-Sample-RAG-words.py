from vertexai.language_models import TextEmbeddingModel
import json

def embed_01():
    text = "a"
    text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=1)
    print(f"text :{text}")
    print(f"Embeddings :{embeddings}")
    print()

def embed_02_twice():
    text = "a"
    print(f"text :{text}")
    text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=1)
    print(f"Embedding  1st time :{embeddings}")
    print()

    embeddings = text_embedding_model.get_embeddings([text], output_dimensionality=1)
    print(f"Embeddings 2nd time:{embeddings}")
    print()

def embed_03_dimentionality():
    text1 = "a"
    text2 = "b"
    print(f"Embedding  for {text1} {text2}")
    text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = text_embedding_model.get_embeddings([text1, text2], output_dimensionality=1)
    print(f"Embeddings :{embeddings}")
    print()

    print(f"Embedding  for {text1} {text2}")
    embeddings = text_embedding_model.get_embeddings([text1, text2], output_dimensionality=1)
    print(f"Embeddings :{embeddings}")
    print()

def embed_04():
    text1 = "a"
    print(f"Embedding  for {text1}")
    text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = text_embedding_model.get_embeddings([text1], output_dimensionality=2)
    print(f"Type :{type(embeddings)}, {len(embeddings)}")
    print(f"Embeddings :{embeddings}")
    print(f"embeddings 0 stats  :{embeddings[0].statistics}")
    print(f"embeddings 0 values :{embeddings[0].values}")
    
    print()


def embed_05_no_dimenality():
    text1 = "a"
    print(f"Embedding  for {text1}")
    text_embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = text_embedding_model.get_embeddings([text1])
    print(f"Type :{type(embeddings)}, {len(embeddings)}")
    print(f"Embeddings :{embeddings}")
    print(f"embeddings 0 stats  :{embeddings[0].statistics}")
    print(f"embeddings 0 values :{embeddings[0].values}")
    
    print()
  
def main():
    # embed_01()
    # embed_02_twice()
    # embed_03_dimentionality()
    # embed_04()
    embed_05_no_dimenality()
    pass
    
if __name__ == "__main__":
    main()
