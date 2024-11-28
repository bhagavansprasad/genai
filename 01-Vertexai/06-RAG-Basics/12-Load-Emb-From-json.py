import pandas as pd

def load_embeddings_from_json(text_embeddings_json):
    dataframe = pd.read_json(text_embeddings_json)

    return dataframe

def main():
    json_embeddings = 'embeddings/cholas.json'
 
    text_df = load_embeddings_from_json(json_embeddings)

    print(text_df.head()) 
    print(text_df.columns)

    return True
  
if __name__ == "__main__":
    main()
    
