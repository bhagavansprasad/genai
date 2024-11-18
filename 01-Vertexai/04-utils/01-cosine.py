from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
tlist = [ 
            [[1, 2, 3], [4, 5, 6]],
            [[1, 2, 3], [1, 2, 3]],
            [[1, 2, 3], [1, 2, 4]],
            [[11, 28, 96], [1, 2, 3]],
        ]
def main():
    for row in tlist:
        a, b = row
        # Example vectors
        vector_a = np.array(a)
        vector_b = np.array(b)

        # Calculate cosine similarity
        cosine_sim = cosine_similarity([vector_a], [vector_b])
        print(f"{cosine_sim} -->[{a}], [{b}]")
        
    
if __name__ == "__main__":
    main()


