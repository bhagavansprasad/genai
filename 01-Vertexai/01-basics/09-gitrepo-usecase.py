# https://github.com/bhagavansprasad/aura_pytest.git
# git@github.com:bhagavansprasad/aura_pytest.git

import os
from google.cloud import storage
from vertexai.generative_models import GenerativeModel

def list_files_in_gcs_folder(bucket_name, folder_name, output_file):
    code_index = []
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=folder_name)
    
    if os.path.exists(output_file):
        os.remove(output_file)
        
    with open(output_file, 'a') as output:
        for blob in blobs:
            # Download the blob content as a string
            content = blob.download_as_text()
            
            # Append the file name and content to the output file
            code_index.append(blob.name)

            output.write(f"\n--- File: {blob.name} ---\n")
            output.write(content)
            output.write("\n--- End of File ---\n")

    print(f"Appended all files from '{folder_name}' to '{output_file}'")
    
    return code_index


def get_code_prompt(question, code_index, data):
    """Generates a prompt to a code related question."""

    prompt = f"""
    Questions: {question}

    Context:
    - The entire codebase is provided below.
    - Here is an index of all of the files in the codebase:
      \n\n{code_index}\n\n.
    - Then each of the files is concatenated together. You will find all of the code you need:
      \n\n{data}\n\n

    Answer:
    """
    return prompt

def gitrepo_create_documentaion():
    bucket_name = "bhagavan-pub-bucket"
    folder_name = "aura_pytest/"
    output_file = "new.txt"
    
    code_index = list_files_in_gcs_folder(bucket_name, folder_name, output_file)
    
    with open(output_file) as fd:
        data = fd.read()
    
    # print(f"data :{data}")

    question = """
    Provide a documentation and starting guide to new developers who is onboarding to the codebase.
    """    
    prompt = get_code_prompt(question, code_index, data)
    
    contents = [prompt]

    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    

    response = multimodal_model.generate_content(contents)
    print(response.text)

    return

def gitrepo_create_summary():
    bucket_name = "bhagavan-pub-bucket"
    folder_name = "aura_pytest/"
    output_file = "new.txt"
    
    code_index = list_files_in_gcs_folder(bucket_name, folder_name, output_file)
    
    with open(output_file) as fd:
        data = fd.read()
    
    # print(f"data :{data}")

    question = """
        Give me a summary of this codebase, and tell me the top 3 things that I can learn from it.
    """    
    prompt = get_code_prompt(question, code_index, data)
    
    contents = [prompt]

    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    

    response = multimodal_model.generate_content(contents)
    print(response.text)

    return

def gitrepo_find_bugs():
    bucket_name = "bhagavan-pub-bucket"
    folder_name = "aura_pytest/"
    output_file = "new.txt"
    
    code_index = list_files_in_gcs_folder(bucket_name, folder_name, output_file)
    
    with open(output_file) as fd:
        data = fd.read()
    
    question = """
        Can you list top 3 bugs in the codebase?
    """    
    prompt = get_code_prompt(question, code_index, data)
    
    contents = [prompt]

    model = "gemini-1.5-pro-001"
    multimodal_model = GenerativeModel(model)    

    response = multimodal_model.generate_content(contents)
    print(response.text)

    return

def main():
    # gitrepo_create_documentaion()
    # gitrepo_create_summary()
    gitrepo_find_bugs()
    
  
if __name__ == "__main__":
    main()
    pass
