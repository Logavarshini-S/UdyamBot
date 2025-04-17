import csv
import json
import re

# File paths
input_csv = "msme_schemes_raw_pages3to51.csv"
output_json = "final_msme_schemes.json"

# Keywords used to detect sections
section_keywords = {
    "description": ["Objective"],
    "eligibility": ["Scheme applicable for", "Who can apply", "Eligibility"],
    "benefits": ["Nature of assistance", "Benefits"],
    "how_to_apply": ["How to apply", "Apply on", "Application process"]
}

# Function to extract structured fields from raw text
def extract_fields(raw_text):
    scheme = {
        "scheme_name": "",
        "description": "",
        "eligibility": "",
        "benefits": "",
        "how_to_apply": ""
    }

    lines = raw_text.strip().split("\n")
    scheme["scheme_name"] = lines[0].strip() if lines else "Untitled Scheme"

    full_text = "\n".join(lines[1:])

    # For each field, try to extract content using regex
    for field, keys in section_keywords.items():
        for keyword in keys:
            pattern = rf"{keyword}[:\n](.*?)(?=\n(?:{'|'.join(sum(section_keywords.values(), []))})[:\n]|$)"
            match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
            if match:
                scheme[field] = match.group(1).strip().replace('\n', ' ')
                break

    return scheme

# Process the CSV
schemes = []

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        raw_text = row["raw_text"]
        if len(raw_text.strip()) > 100:  # skip very short entries
            scheme = extract_fields(raw_text)
            schemes.append(scheme)

# Save to JSON
with open(output_json, "w", encoding="utf-8") as jsonfile:
    json.dump(schemes, jsonfile, indent=2, ensure_ascii=False)

print(f"✅ Converted to structured JSON and saved as '{output_json}'")
