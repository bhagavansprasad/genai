import time
import requests
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate


def list_py_files_github(repo_owner, repo_name, branch="main"):
    # GitHub API URL to fetch the repository contents
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{branch}?recursive=1"
    ftype = "py"
    
    try:
        # Send a GET request to the GitHub API to fetch the repository's file tree
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        repo_tree = response.json()

        # Base URL for the raw files
        raw_base_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/"

        # List to store all .ipynb files
        py_files = []

        # Traverse the tree and find .ipynb files
        for item in repo_tree.get('tree', []):
            if item['path'].endswith(f'.{ftype}'):
                file_path = item['path']
                file_url = raw_base_url + file_path
                py_files.append({"file" : file_path, "url" :file_url})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repository data: {e}")
    
    return py_files


def get_file_content_from_url(file_url):
    try:
        # Send a GET request to fetch the file content
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Return the content of the file
        return response.text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the file from URL: {e}")
        return None

def create_docs_from_sources(source_files):
    docs_list = []
    for i, file in enumerate(source_files, 1):
        content = get_file_content_from_url(file['url'])

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

def get_texts_by_git_repo():
    repo_owner = "bhagavansprasad"
    repo_name = "pdbwhereami"
    branch = "main"  # Specify the branch name, default is 'main'

    code_files_urls = list_py_files_github(repo_owner, repo_name, branch)
    docs_list = create_docs_from_sources(code_files_urls)

    texts = text_split_to_embend(docs_list)
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
    # RAG template
    prompt_RAG = """
        You are a proficient python developer. Respond with the syntactically correct code for to the question below. Make sure you follow these rules:
        1. Use context to understand the APIs and how to use it & apply.
        2. Do not add license information to the output code.
        3. Do not include Colab code in the output.
        4. Ensure all the requirements in the question are met.

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
    print(results["result"])


# Create Code LLM
code_llm = VertexAI(model_name="gemini-1.5-pro", max_output_tokens=2048, temperature=0.1, verbose=False)
    
def main():
    texts = get_texts_by_git_repo()
    print(f"Len of texts :{len(texts)}")
    
    db = create_text_embeddings(texts)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 5}) 
    
    ask_question_01(retriever)
  
if __name__ == "__main__":
    main()
    pass
