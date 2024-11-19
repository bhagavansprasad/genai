import fitz

def create_pdf_with_fitz(output_path, content):
    # Create a new PDF document
    pdf_document = fitz.open()

    # Add a page to the document
    page = pdf_document.new_page()

    # Define text settings
    font_size = 12
    x, y = 50, 50  # Starting coordinates for text
    line_height = font_size + 2

    # Split the content into lines and add to the page
    for line in content.split("\n"):
        line = line.strip()
        page.insert_text((x, y), line, fontsize=font_size)
        y += line_height  # Move to the next line

    # Save the document to the specified path
    pdf_document.save(output_path)
    pdf_document.close()

    print(f"PDF created successfully at: {output_path}")

# 1. Open and Close Document
def open_pdf(file_path):
    pdf = fitz.open(file_path)
    print(f"Opened PDF with {len(pdf)} pages.")
    pdf.close()

# 2. Access Pages
def get_page(file_path, page_number):
    pdf = fitz.open(file_path)
    page = pdf[page_number]
    print(page)
    pdf.close()

# 3. Extract Text
def extract_text(file_path):
    pdf = fitz.open(file_path)
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        print(f"Page {page_number + 1}:\n{page.get_text()}")
    pdf.close()

# 4. Get Metadata
def get_metadata(file_path):
    pdf = fitz.open(file_path)
    metadata = pdf.metadata
    print("Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
    pdf.close()

# 5. Get Number of Pages
def get_page_count(file_path):
    pdf = fitz.open(file_path)
    print(f"Number of pages: {len(pdf)}")
    pdf.close()

# 6. Search for Text
def search_text(file_path, keyword):
    pdf = fitz.open(file_path)
    page = pdf[0]
    results = page.search_for(keyword)
    print(f"Found {len(results)} occurrences of '{keyword}' on the first page.")
    pdf.close()

# 7. Extract Images
def extract_images(file_path):
    pdf = fitz.open(file_path)
    page = pdf[0]
    images = page.get_images()
    print(f"Found {len(images)} images on the first page.")
    pdf.close()

# 8. Render Page as Image
def render_page_as_image(file_path, page_number, output_path):
    pdf = fitz.open(file_path)
    pixmap = pdf[page_number].get_pixmap()
    pixmap.save(output_path)
    print(f"Page {page_number + 1} saved as an image: {output_path}")
    pdf.close()

# 9. Annotate Pages
def highlight_text(file_path, keyword, output_path):
    pdf = fitz.open(file_path)
    page = pdf[0]
    highlights = page.search_for(keyword)
    for rect in highlights:
        page.add_highlight_annot(rect)
    pdf.save(output_path)
    print(f"Saved highlighted PDF to {output_path}")
    pdf.close()

# 10. Insert Pages
def insert_page(file_path, text, output_path):
    pdf = fitz.open(file_path)
    pdf.insert_page(0, text=text)
    pdf.save(output_path)
    print(f"Inserted a new page with text and saved to {output_path}")
    pdf.close()

# 11. Merge PDFs
def merge_pdfs(pdf1_path, pdf2_path, output_path):
    pdf1 = fitz.open(pdf1_path)
    pdf2 = fitz.open(pdf2_path)
    pdf1.insert_pdf(pdf2)
    pdf1.save(output_path)
    print(f"Merged PDFs and saved to {output_path}")
    pdf1.close()
    pdf2.close()

# 12. Save PDF
def save_pdf_with_compression(file_path, output_path):
    pdf = fitz.open(file_path)
    pdf.save(output_path, deflate=True)
    print(f"Saved compressed PDF to {output_path}")
    pdf.close()

# 13. Delete Pages
def delete_page(file_path, page_number, output_path):
    pdf = fitz.open(file_path)
    pdf.delete_page(page_number)
    pdf.save(output_path)
    print(f"Deleted page {page_number + 1} and saved to {output_path}")
    pdf.close()

# 14. Extract Table of Contents
def extract_toc(file_path):
    pdf = fitz.open(file_path)
    toc = pdf.get_toc()
    print("Table of Contents:")
    for entry in toc:
        print(entry)
    pdf.close()

# 15. Extract Links
def extract_links(file_path):
    pdf = fitz.open(file_path)
    page = pdf[0]
    links = page.get_links()
    print("Links on the first page:")
    for link in links:
        print(link)
    pdf.close()

# Main function to demonstrate usage
def main():
    file_path = "bits.pdf"
    keyword = "swap"
    output_image_path = "page1.png"
    output_pdf_path = "output.pdf"

    output_file = "ramayan.pdf"
    text_content = """Ramayan is an ancient Indian epic.
    It narrates the journey of Lord Rama.
    The story includes Sita, Lakshman, Hanuman.
    Written by sage Valmiki in Sanskrit.
    """
    create_pdf_with_fitz(output_file, text_content)
    return

    # Call any of the defined functions
    # Example calls:
    open_pdf(file_path)
    get_page_count(file_path)
    extract_text(file_path)
    get_metadata(file_path)
    search_text(file_path, keyword)
    extract_images(file_path)
    render_page_as_image(file_path, 0, output_image_path)
    highlight_text(file_path, keyword, output_pdf_path)
    insert_page(file_path, "This is a new page", output_pdf_path)
    merge_pdfs("bits.pdf", "output.pdf", "merged.pdf")
    save_pdf_with_compression(file_path, "compressed.pdf")
    delete_page(file_path, 0, output_pdf_path)
    extract_toc(file_path)
    extract_links(file_path)


if __name__ == "__main__":
    main()
    
