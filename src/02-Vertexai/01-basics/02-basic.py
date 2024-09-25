from vertexai.generative_models import GenerativeModel

def hello_world():
    model = GenerativeModel("gemini-pro")
    retval = model.generate_content("Why is Sky is blue?")

    print(f"retval text :{retval.text}")


def main():
    hello_world()
    

if __name__ == "__main__":
    main()