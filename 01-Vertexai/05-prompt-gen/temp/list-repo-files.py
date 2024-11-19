
from pathlib import Path

def list_specific_files_in_repo(repo_path):
    repo = Path(repo_path)
    allowed_extensions = {".docx", ".pdf", ".html"}  # Allowed file extensions
    all_files = [
        str(file)
        for file in repo.rglob('*')
        if file.is_file() and file.suffix in allowed_extensions and '.git' not in file.parts
    ]
    return all_files


# Example usage
repo_path = "/home/bhagavan/test_repos/repos"
files = list_specific_files_in_repo(repo_path)
print(f"Found {len(files)} files:")
for file in files:
    print(file)
