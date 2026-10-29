from langchain_google_vertexai import VertexAI  # Correct import
VertexAI.model_rebuild()  # Still important

llm = VertexAI(model_name="gemini-1.5-pro")

prompt = "Write a short story about a robot learning to love."
generated_text = llm(prompt)

print(generated_text)

