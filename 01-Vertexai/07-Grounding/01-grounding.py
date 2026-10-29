import vertexai

from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Tool,
    grounding,
)

# Initialize Vertex AI
PROJECT_ID = "your-project-id"
vertexai.init(project=PROJECT_ID, location="us-central1")

# Create a GenerativeModel object
model = GenerativeModel("gemini-1.5-flash-001")

# Define a grounding tool for Google Search
tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

# Create a GenerationConfig object
generation_config = GenerationConfig(temperature=0.0)

# Prompt for grounding
prompt = "When is the next total solar eclipse in US?"

# Generate content using the model and grounding tool
response = model.generate_content(
    prompt, tools=[tool], generation_config=generation_config
)

print(response.text)