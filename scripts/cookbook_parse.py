import fitz  # PyMuPDF
import os
import re
import html

def clean_pdf_text(text: str) -> str:
    # Decode HTML entities (just in case)
    text = html.unescape(text)
    # Remove control characters and non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", " ", text)
    # Replace standalone keywords like 'del', 'null', 'None' with 'NA'
    text = re.sub(r"\b(null|None|del)\b", "NA", text, flags=re.IGNORECASE)
    # Strip excessive whitespace
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

def parse_cookbook(pdf_name):
    pdf_path = f"cookbooks/pdfs/{pdf_name}"

    # Get basename without extension
    name = pdf_name.split(".")[0]

    output_dir = f"cookbooks/txt/{name}"
    os.makedirs(output_dir, exist_ok=True)

    # Load the PDF
    doc = fitz.open(pdf_path)

    # Loop through pages and save cleaned text
    for i, page in enumerate(doc):
        raw_text = page.get_text()
        cleaned_text = clean_pdf_text(raw_text)
        
        filename = os.path.join(output_dir, f"page_{i+1}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Saved Page {i+1} to {filename}")
