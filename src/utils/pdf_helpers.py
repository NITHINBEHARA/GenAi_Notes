import os
import fitz  # PyMuPDF

def inspect_pdf_page(pdf_path, page_num):
    """Prints extracted text and image count for a specific page."""
    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return

    doc = fitz.open(pdf_path)
    if 1 <= page_num <= len(doc):
        page = doc.load_page(page_num - 1)
        text = page.get_text()
        print(f"\n--- {os.path.basename(pdf_path)} | Page {page_num} Content ---")
        print(text if text.strip() else "[No text layer found]")
        print("-" * 40)
        print(f"Text Length: {len(text)}")
        print(f"Images: {len(page.get_images())}")
    else:
        print(f"Error: Page {page_num} is out of range (Total pages: {len(doc)})")
    doc.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        path = sys.argv[1]
        pnum = int(sys.argv[2])
        inspect_pdf_page(path, pnum)
    else:
        print("Usage: python pdf_helpers.py <path_to_pdf> <page_number>")
