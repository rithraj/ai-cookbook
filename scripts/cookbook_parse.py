import fitz  # PyMuPDF
import os

def parse_cookbook(pdf_name):
    pdf_path = f"cookbooks/pdfs/{pdf_name}"

    # Get basename without extension
    name = pdf_name.split(".")[0]

    output_dir = f"cookbooks/txt/{name}"
    os.makedirs(output_dir, exist_ok=True)

    # Load the PDF
    doc = fitz.open(pdf_path)

    # Loop through pages and save text
    for i, page in enumerate(doc):
        text = page.get_text()
        filename = os.path.join(output_dir, f"page_{i+1}.txt")
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Saved Page {i+1} to {filename}")
