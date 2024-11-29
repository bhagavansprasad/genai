from embeddings_utils import get_texts_embeddings
from embeddings_utils import get_pdf_page_embeddings
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    file_obj_embed = []
    logging.debug("Main function started")
    pdf_file_path = "user_data/cholas.pdf" 

    page_embedings, text_bytes = get_pdf_page_embeddings(pdf_file_path)
    logging.debug(f"Retrieved text from PDF of length: {len(text_bytes)}")

    file_embed = get_texts_embeddings(text_bytes)
    logging.debug(f"Generated embeddings dictionary with text length: {len(file_embed['text'])} and embedding length: {len(file_embed['text-embedding'])}")

    file_obj_embed.append({'file': pdf_file_path, 'page_emb': page_embedings, 'file_embd': file_embed})
    
    for file_obj in file_obj_embed:
        print()
        print(f"{file_obj['file']}: Page text and Embeddings....")
        for p in file_obj['page_emb']:
            print(f"\tPage Number :{p['page_number']}")
            print(f"\tPage Text :{p['text'][:20]}...(truncated to 30 bytes)..len :{len(p['text'])}")
            print(f"\tPage text embed :{p['text-embedding'][:5]}...(truncated for brevity)")
            print()
        print(f"\tFile text :{file_obj['file_embd']['text'][:20]}...(truncated to 50 bytes)...len :{len(file_obj['file_embd']['text'])}")
        print(f"\tFile Embeddings :{file_embed['text-embedding'][:5]}...(truncated for brevity)")
        print()
        
    return


if __name__ == "__main__":
    main()
