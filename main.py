from from_text import english_book_helper
from from_text import merge_pdfs_with_margin

if __name__ == "__main__":
    pdf_name = 'cp1.pdf'
    english_book_helper("chapters/" + pdf_name, "output/output_" + pdf_name)
    merge_pdfs_with_margin("chapters/" + pdf_name, "output/output_" + pdf_name, "merged/merged_" + pdf_name, margin=1)