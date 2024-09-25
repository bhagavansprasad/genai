from vertexai.generative_models import GenerativeModel
from vertexai.generative_models import GenerationConfig

def prompt_design_01():
    print("-" * 75)
    prompt = "Describe what is Jai Sriram"
    
    model = GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(prompt)
    
    print(f"Prompt :{prompt}")
    print(f"Response :\n{response.text}")
    print("-" * 75)

def prompt_with_temparature_01():
    print("-" * 75)
    prompt = "Describe what is Jai Sriram"
    gen_config = GenerationConfig(temperature=1.0)
    
    model = GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(prompt, generation_config=gen_config)
    
    print(f"Prompt temparature(1.0):{prompt}")
    print(f"Response :\n{response.text}")
    print("-" * 75)

def prompt_with_temparature_02():
    print("-" * 75)
    prompt = "Describe what is Jai Sriram"
    gen_config = GenerationConfig(temperature=1.0)
    
    model = GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(prompt, generation_config=gen_config)
    
    print(f"Prompt temparature(1.0):{prompt}")
    print(f"Response :\n{response.text}")
    print("-" * 75)

def prompt_with_temparature_03():
    print("-" * 75)
    prompt = "Describe what is Jai Sriram"
    gen_config = GenerationConfig(temperature=0.1)
    
    model = GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(prompt, generation_config=gen_config)
    
    print(f"Prompt temparature(0.1):{prompt}")
    print(f"Response :\n{response.text}")
    print("-" * 75)

def prompt_with_temparature_04():
    print("-" * 75)
    prompt = "Describe what is Jai Sriram"
    gen_config = GenerationConfig(temperature=0.1)
    
    model = GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(prompt, generation_config=gen_config)
    
    print(f"Prompt temparature(0.1):{prompt}")
    print(f"Response :\n{response.text}")
    print("-" * 75)

def main():
    prompt_design_01()
    prompt_with_temparature_01()
    prompt_with_temparature_02()
    prompt_with_temparature_03()
    prompt_with_temparature_04()
    
if __name__ == "__main__":
    main()
