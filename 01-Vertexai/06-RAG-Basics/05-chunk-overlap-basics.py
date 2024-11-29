from embeddings_utils import get_pdf_text_chunks

def main():
    pdf_file_path = "user_data/ramayan.pdf"  
    chunks = get_pdf_text_chunks(pdf_file_path, page_number=0, chunk_size=30, overlap=5)
    
    print(f"Total Chunks: {len(chunks)}\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} - len :{len(chunk)}:\n{chunk}\n")

if __name__ == "__main__":
    main()
    

