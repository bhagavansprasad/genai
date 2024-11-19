from pathlib import Path

def list_files_in_git_repo(repo_path):
    repo = Path(repo_path)
    all_files = [
        str(file)
        for file in repo.rglob('*')
        if file.is_file() and '.git' not in file.parts
    ]
    return all_files


def main():
    base_dir_path = "/home/bhagavan/test_repos"
    files = list_files_in_git_repo(base_dir_path)

    print(f"Found {len(files)} files in :{base_dir_path}")
    for i, file in enumerate(files, 1):
        print(f"\t{i}. {file}")

    print()
  
if __name__ == "__main__":
    main()
    
