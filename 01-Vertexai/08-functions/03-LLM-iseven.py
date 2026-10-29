import os
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

MODEL = "gemini-1.5-pro-001"
CONFIG = GenerationConfig(temperature=0)

def validate(model, prompt):
    print(f"{prompt}")
    response = model.generate_content(prompt)
    print(response.text)
    print()

def main():
    model = GenerativeModel(MODEL, generation_config=CONFIG)
    
    prompt = "is 9 even?"
    validate(model, prompt)

    prompt = "is nine even?"
    validate(model, prompt)

    prompt = "10 is even?"
    validate(model, prompt)

    prompt = "Is abc even?"
    validate(model, prompt)

if __name__ == "__main__":
    main()
