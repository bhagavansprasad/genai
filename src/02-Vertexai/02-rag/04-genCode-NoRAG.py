import time
import requests
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os

def list_py_files(directory):
    # List to store all .py file paths
    py_files = []

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        # Filter for .py files
        for file in files:
            if file.endswith(".py"):
                # py_files.append(os.path.join(root, file))
                py_files.append({"file" : file, "url" :os.path.join(root, file)})

    return py_files

def read_file_content(file_path):
    try:
        # Open the file in read mode and read its content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None


def create_docs_from_sources(source_files):
    docs_list = []

    for i, file in enumerate(source_files, 1):
        content = read_file_content(file['url'])

        doc = Document(
            page_content=content,
            metadata={
                "url": file['url'],
                "file_index": i 
            }
        )

        docs_list.append(doc)
        
    return docs_list

def text_split_to_embend(docs_list):
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=2000,
        chunk_overlap=200
    )

    texts = text_splitter.split_documents(docs_list)
    
    return texts

def get_texts_by_local_folder():
    directory = "/home/bhagavan/my-git-repos/pdbwhereami"  # Replace with your directory path
    code_files = list_py_files(directory)

    print("Source files to create embeddings")
    for file in code_files:
        print(f"\t{file['url']}")
    
    docs_list = create_docs_from_sources(code_files)
    texts = text_split_to_embend(docs_list)
    
    print()
    return texts

# Rate Limiter function
def rate_limit(max_per_minute):
    period = 60 / max_per_minute
    print("Waiting")
    while True:
        before = time.time()
        yield       # Request making happens here
        after = time.time()
        elapsed = after - before
        sleep_time = max(0, period - elapsed)
        if sleep_time > 0:
            print(".", end="")
            time.sleep(sleep_time)
            
class CustomVertexAIEmbeddings(VertexAIEmbeddings):
    requests_per_minute: int
    num_instances_per_batch: int
    model_name: str
    
    def embed_documents(self, texts: list[str], batch_size: int = 0) -> list[list[float]]:
        # setup rate limiter
        limiter = rate_limit(self.requests_per_minute)
        
        results = []
        
        docs = list(texts)
        
        while docs:
            head, docs = (
                docs[: self.num_instances_per_batch],
                docs[self.num_instances_per_batch : ]
            )
            chunk = self.client.get_embeddings(head)
            results.extend(chunk)
            next(limiter)
        
        return [r.values for r in results]

def create_text_embeddings(texts):
    embeddings = CustomVertexAIEmbeddings(requests_per_minute = 100, num_instances_per_batch = 5, model_name = "textembedding-gecko@latest")
    # Create Index from embedded code chunks
    db = FAISS.from_documents(texts, embeddings)
    
    return db

def ask_question_01(retriever):
    # Create Code LLM
    code_llm = VertexAI(model_name="gemini-1.5-pro", max_output_tokens=2048, temperature=0.1, verbose=False)
    
    # RAG template
    prompt_RAG = """
        You are a proficient python developer. Respond with the syntactically correct code for to the question below. Make sure you follow these rules:
        1. Use context to understand the APIs and how to use it & apply.
        2. Do not add license information to the output code.
        3. Do not include Colab code in the output.
        4. Ensure all the requirements in the question are met.
        5. Debug functions that are defined in pdbwhereami module 

        Question:
        {question}

        Context:
        {context}

        Helpful Response :
        """

    prompt_RAG_template = PromptTemplate(template=prompt_RAG, input_variables=["context", "question"])
    

    qa_chain = RetrievalQA.from_llm(llm=code_llm, prompt=prompt_RAG_template, retriever=retriever, return_source_documents=True ) 
    
    user_question = "Create a Python function with debug statement using pdbwhereami moduel to print Line number, functio name, and call stack at appropriate places in the function"
    results = qa_chain.invoke(input={"query": user_question})
    print(results.keys())
    print(f"Query       :{results['query']}")
    print(f"Source docs : {type(results['source_documents'])}")
    # print(f"Source docs : {results['source_documents']}")
    print(f"Result      : {results['result']}")

def main():
    code_llm = VertexAI(model_name="gemini-1.5-pro", max_output_tokens=2048, temperature=0.1, verbose=False)

    user_question = "Create a Python function with debug statement using pdbwhereami moduel to print Line number, functio name, and call stack at appropriate places in the function"

    response = code_llm.invoke(input=user_question, max_output_tokens=2048, temperature=0.1)
    print(response)
  
if __name__ == "__main__":
    main()
