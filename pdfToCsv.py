import fitz  # PyMuPDF
import csv

# Load PDF file
pdf_path = "MSMESchemebooklet2024.pdf"
doc = fitz.open(pdf_path)

# Define page range (pages 3 to 51 inclusive, 0-based index is 2 to 50)
start_page = 2
end_page = 51

# Extract text from each page
extracted_pages = []
for i in range(start_page, end_page):
    text = doc.load_page(i).get_text()
    extracted_pages.append({
        "page_number": i + 1,
        "raw_text": text.strip()
    })

# Output CSV file
csv_path = "msme_schemes_raw_pages3to51.csv"

with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["page_number", "raw_text"])
    writer.writeheader()
    for entry in extracted_pages:
        writer.writerow(entry)

print(f"✅ PDF converted and saved to '{csv_path}'")
