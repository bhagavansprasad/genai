from dump_utils import smart_print_with_list_trimming
from embeddings_utils import get_pdf_embeddings

import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    file_obj_embed = []
    logging.debug("Main function started")
    pdf_file_path = "user_data/cholas.pdf" 
    
    doc_embeddings = get_pdf_embeddings(pdf_file_path)
    smart_print_with_list_trimming(doc_embeddings)
    
if __name__ == "__main__":
    main()

