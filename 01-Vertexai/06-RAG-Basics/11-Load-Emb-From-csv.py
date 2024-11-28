import pandas as pd
    
def load_embeddings_from_csv(csv_embeddings):
    dataframe  = pd.read_csv(csv_embeddings)
    return dataframe

def main():
    csv_embeddings = 'embeddings/cholas.csv'
 
    text_df = load_embeddings_from_csv(csv_embeddings)

    print(text_df.head()) 
    print(text_df.columns)
    print(text_df.columns)

    return True
  
if __name__ == "__main__":
    main()
