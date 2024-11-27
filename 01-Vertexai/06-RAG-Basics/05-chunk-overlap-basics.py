import fitz

def create_chunks_with_overlap(pdf_path, page_number=0, chunk_size=10, overlap=3):
    chunks = []
    
    # Open the PDF and read the specified page
    with fitz.open(pdf_path) as pdf:
        if page_number >= len(pdf):
            raise ValueError("Page number exceeds the number of pages in the PDF.")
        
        page = pdf[page_number]
        text = page.get_text("text")  # Extract text from the page
    
    # Remove any extra whitespace and convert to bytes
    text_bytes = text.encode('utf-8')
    
    print(f"File content, len :{len(text_bytes)}")
    print(f"{text_bytes}\n")
    
    # Create chunks with overlap
    for i in range(0, len(text_bytes) - chunk_size + 1, chunk_size - overlap):
        chunks.append(text_bytes[i:i + chunk_size].strip())
    
    chunks.append(text_bytes[i+chunk_size:].strip())
    return [chunk.decode('utf-8', errors='ignore') for chunk in chunks]

# Example usage
def main():
    pdf_file_path = "user_data/ramayan.pdf"  # Replace with your PDF file path
    chunks = create_chunks_with_overlap(pdf_file_path, page_number=0, chunk_size=30, overlap=5)
    
    print(f"Total Chunks: {len(chunks)}\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} - len :{len(chunk)}:\n{chunk}\n")

if __name__ == "__main__":
    main()
    

