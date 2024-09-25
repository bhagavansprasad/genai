
# https://github.com/bhagavansprasad/aura_pytest.git
# git@github.com:bhagavansprasad/aura_pytest.git

import requests
import os
import time

# Crawl through git repo and return list of all ipynb files in the repo.
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
        if (item["type"] == "file"
            and (item["name"].endswith(".py") or item["name"].endswith(".ipynb"))
        ):
            files.append(item["html_url"])
        elif item["type"] == "dir" and not item["name"].startswith("."):
            sub_files = crawl_git_repo(item["url"], True, access_token)
            time.sleep(0.1)         # Wait for 100 milliseconds before next github api call.
            files.extend(sub_files)

    return files


def main():
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    print(GITHUB_TOKEN)
    REPO_URL = "ibm-et/jupyter-samples"
    code_files_urls = crawl_git_repo(REPO_URL, False, GITHUB_TOKEN)
    print(code_files_urls)
    
    for file in code_files_urls:
        print(file)

    # list_ipynb_files()
    
  
if __name__ == "__main__":
    main()
    pass
