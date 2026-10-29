import os
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.environ['PROJECT_ID']
LOCATION = os.environ['LOCATION_ID']

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    "What are the latest features of our new product?",
    grounding="projects/your-project-id/locations/us-central1/knowledgeBases/product_info"
)

print(response.text)
