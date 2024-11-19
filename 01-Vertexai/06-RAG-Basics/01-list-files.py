from pathlib import Path

def list_all_files(directory_path):
    directory = Path(directory_path)
    all_files = [str(file) for file in directory.rglob('*') if file.is_file()]
    return all_files

def main():
    base_dir_path = "/home/bhagavan/test_repos"
    files = list_all_files(base_dir_path)

    print(f"Found {len(files)} files in :{base_dir_path}")
    for file in files:
        print(f"{file}")
        
    print()

    print(f"Found {len(files)} files in :{base_dir_path}")
    for i, file in enumerate(files, 1):
        print(f"\t{i}. {file}")
  
if __name__ == "__main__":
    main()
    
