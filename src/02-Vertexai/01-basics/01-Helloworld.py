import vertexai
from vertexai.generative_models import GenerativeModel

model = vertexai.generative_models.GenerativeModel("gemini-pro")

model = vertexai.generative_models.GenerativeModel("gemini-1.5-pro-001")
response = model.generate_content("Explain LLM")

print(response.text)