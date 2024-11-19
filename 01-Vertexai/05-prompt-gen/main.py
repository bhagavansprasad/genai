import os
import time
import requests 
import json
from pathlib import Path
from typing import Dict

import torch
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredHTMLLoader
from langchain_huggingface import HuggingFaceEmbeddings
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
)

def _is_text_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            # Try reading a small chunk from the file.
            file.read(1024)
            return True
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        # File is not a file text file, doesn't exist, or it is a directory.
        return False

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logging.debug(f"Folder created: {folder_path}")
    else:
        logging.debug(f"Folder already exists: {folder_path}")
        
    return Path(folder_path)

def list_specific_files_in_repo(repo_path):
    repo = Path(repo_path)
    allowed_extensions = {".docx", ".pdf", ".html"}  # Allowed file extensions
    all_files = [
        str(file)
        for file in repo.rglob('*')
        if file.is_file() and file.suffix in allowed_extensions and '.git' not in file.parts
    ]
    return all_files

class RAGManager:
    base_dir = None
    cache_dir = None
    vectordb_dir = None
    
    def __init__(self, base_dir_path, repos_path, cache_path, vectdb_path):
        if not os.path.exists(base_dir_path):
            logging.debug(f"{base_dir_path} Doesnot exists")
            return None
        
        self.base_dir = Path(base_dir_path)

        if not os.path.exists(self.base_dir / repos_path):
            logging.debug(f"{base_dir_path}/{repos_path} Doesnot exists")
            return None

        self.repos_dir = self.base_dir / repos_path
        self.cache_dir = create_folder_if_not_exists(self.base_dir / cache_path)
        self.vectordb_dir = create_folder_if_not_exists(self.base_dir / vectdb_path)
        
        return
        # Check for GPU availability. If not available, go with CPU.
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.debug(f"Using device: {self.device}")
        logging.debug(f"CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            logging.debug(f"GPU Name: {torch.cuda.get_device_name(0)}")
            logging.debug(f"GPU count: {torch.cuda.device_count()}")

        # Initialize Embedding model.
        # NOTE: Use "all-mpnet-base-v2" if you have good processing environment, else use "all-MiniLM-L6-v2".
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": self.device}
        )

        # Configure File Loaders
        self.loader_mapping = {
            ".pdf": PyPDFLoader,
            ".docx": UnstructuredWordDocumentLoader,
            ".html": UnstructuredHTMLLoader,
        }

    def process_all_projects(self):
        projects = [directory for directory in self.repos_dir.iterdir()  if directory.is_dir()]
        logging.debug(f"Found {len(projects)} projects to process.")

        for i, project in enumerate(projects, 1):
            logging.debug(f"\t{i}. {project}")
            
        return projects

    def process_project(self, project):
        print()
        logging.debug(f"Processing project: {project.name}")
        repos_dir = self.repos_dir
        project_dir = self.base_dir / "userdata" / "repos"
        docs_dir  =  self.base_dir / "userdata" / "docs"
        
        print(f"\trepos_dir   :{repos_dir}")
        print(f"\tproject_dir :{project_dir}")
        print(f"\tdocs_dir    :{docs_dir}")
        
        # /home/bhagavan/test_repos/userdata/cache/test-repo1.json
        return

        # Create repos and docs directories if they don't exist
        repos_dir.mkdir(parents=True, exist_ok=True)
        docs_dir.mkdir(parents=True, exist_ok=True)

        # Load existing cache
        project_cache = self._load_project_cache(project)

        # Get all project repositories.
        repos = [repo for repo in repos_dir.iterdir() if repo.is_dir()]
        logging.debug(f"Found {len(repos)} repositories to process for project {project.name}.")

        all_files = []
        for repo in repos:
            repo_files = self._get_supported_files(repo)
            logging.debug(f"Found {len(repo_files)} supported files in repository {repo.name}.")
            all_files.extend(repo_files)

        if docs_dir.exists():
            docs_files = self._get_supported_files(docs_dir)
            logging.debug(f"Found {len(docs_files)} supported files in docs directory.")
            all_files.extend(docs_files)

        logging.debug(f"Total files to process: {len(all_files)}")

    def _load_project_cache(self, project) -> Dict[str, str]:
        cache_file = self.cache_dir / f"{project}_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.ERROR(f"Could not load cache for {project}: {e}")
        return {}

    def _get_supported_files(self, repo):
        supported_files = []
        try:
            for file in repo.rglob("*"):
                # Skip hidden files and directories
                if file.name.startswith("."):
                    continue

                if file.is_file():
                    file_extension = file.suffix.lower()
                    if file_extension in self.loader_mapping:
                        supported_files.append(file)
                    elif _is_text_file(file):
                        supported_files.append(file)
                    else:
                        logging.ERROR(f"Unsupported file type: {file_extension}")
        except Exception as e:
            logging.ERROR(f"Could not get supported files for {repo}: {e}")

        return supported_files


def crawl_git_repo(url: str, is_sub_dir: bool, access_token: str):
    if is_sub_dir:
        api_url = url
    else:
        api_url = f"https://api.github.com/repos/{url}/contents"

    header = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {access_token}",
    }
    response = requests.get(api_url, headers=header)

    # Check for any request errors
    response.raise_for_status()

    files = []
    contents = response.json()

    for item in contents:
        if (item["type"] == "file"):
            files.append(item["html_url"])
        elif item["type"] == "dir" and not item["name"].startswith("."):
            sub_files = crawl_git_repo(item["url"], True, access_token)
            time.sleep(0.1)         # Wait for 100 milliseconds before next github api call.
            files.extend(sub_files)

    return files

git_repos = [
    "bhagavansprasad/test-repo1",
    "bhagavansprasad/test-repo2",
    "bhagavansprasad/test-repo3",
]

def main():
    base_dir_path = "/home/bhagavan/test_repos"
    repos_path = "repos"
    cache_dir_path = "userdata/cache"
    vector_db_path = "userdata/vectordb"
    repos_n_files = list(dict())
    
    rag_manager = RAGManager(base_dir_path, repos_path, cache_dir_path, vector_db_path)
    repos = rag_manager.process_all_projects()

    for repo in repos:
        # rag_manager.process_project(repo)
        print(f"repo :{repo}")
        files = list_specific_files_in_repo(repo)
        
        for file in files:
            print(file)
        print()
        
        element = {'repo_name': repo.name, 'path' : repo, 'files' : files}
        repos_n_files.append(element)
    
    print(repos_n_files)
    
  
if __name__ == "__main__":
    main()
    pass
