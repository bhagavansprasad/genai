import logging
from embeddings_utils import get_texts_embeddings
from embeddings_utils import get_pdf_text

logging.basicConfig(level=logging.DEBUG)

def main():
    logging.debug("Main function started")
    pdf_file_path = "user_data/ramayan.pdf"  # Replace with your PDF file path

    text_bytes = get_pdf_text(pdf_file_path)
    logging.debug(f"Retrieved text from PDF of length: {len(text_bytes)}")

    embed_dict = get_texts_embeddings(text_bytes)
    logging.debug(f"Generated embeddings dictionary with text length: {len(embed_dict['text'])} and embedding length: {len(embed_dict['text-embedding'])}")

    print(f"Text...\n{embed_dict['text'][:50]}... (truncated for brevity)")  # Display the first 500 characters
    print(f"Embeddings...\n{embed_dict['text-embedding'][:10]}... (truncated for brevity)")  # Display first 10 embedding values


if __name__ == "__main__":
    main()
