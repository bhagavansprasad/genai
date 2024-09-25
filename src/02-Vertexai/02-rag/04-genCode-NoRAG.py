from langchain_google_vertexai import VertexAI

def main():
    code_llm = VertexAI(model_name="gemini-1.5-pro", max_output_tokens=2048, temperature=0.1, verbose=False)

    user_question = "Create a Python function with debug statement using pdbwhereami moduel to print Line number, functio name, and call stack at appropriate places in the function"

    response = code_llm.invoke(input=user_question, max_output_tokens=2048, temperature=0.1)
    print(response)
  
if __name__ == "__main__":
    main()
