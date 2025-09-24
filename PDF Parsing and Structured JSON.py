import fitz  # PyMuPDF
import pdfplumber
import json
import os
import re

# --------------------------
# PDF file path
# --------------------------
file_path = r"F:\Data Science\ML Projects\PDF Parsing\[Fund Factsheet - May]360ONE-MF-May 2025.pdf.pdf"

# --------------------------
# Clean text lines
# --------------------------
def clean_text(text):
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.lower() in ["page", "|", "page |"] or line.isnumeric():
            continue
        cleaned_lines.append(line)
    return cleaned_lines

# --------------------------
# Determine heading level
# --------------------------
def classify_heading_level(text, font_size):
    """
    Assign heading levels based on font size, style, and content.
    """

    text = text.strip()

    # --- Exclusion patterns (dates, fiscal years, month-year)
    if re.match(r"^(FY\d{2}|\d{4}|[A-Za-z]{3}-\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[- ]?\d{2,4})$", text, re.IGNORECASE):
        return 0  # normal paragraph

    # --- Rule 1: Large font → Section heading
    if font_size >= 14 or text.upper() in ["FUND FACTSHEET", "MONTHLY FACTSHEET", "DISCLAIMER"]:
        return 1  

    # --- Rule 2: Medium font or ALL CAPS → Subsection
    if 12 <= font_size < 14 or text.isupper():
        return 2  

    # --- Rule 3: Short ALL CAPS text → Subsection
    if len(text.split()) <= 4 and text.isupper():
        return 2  

    return 0


def merge_headings(content_list):
    merged_content = []
    buffer = None

    for item in content_list:
        if item["type"] == "section" and buffer and buffer["type"] == "section":
            # merge titles if both are short
            if len(buffer["title"].split()) <= 2 and len(item["title"].split()) <= 2:
                buffer["title"] = buffer["title"] + " " + item["title"]
                continue
            else:
                merged_content.append(buffer)
                buffer = item
        else:
            if buffer:
                merged_content.append(buffer)
            buffer = item

    if buffer:
        merged_content.append(buffer)

    return merged_content



# --------------------------
# Extract hierarchical text
# --------------------------
def extract_hierarchical_text(pdf_path):
    doc = fitz.open(pdf_path)
    all_pages = []

    for page_num, page in enumerate(doc, start=1):
        page_data = {"page_number": page_num, "content": []}
        section_stack = []
        blocks = page.get_text("dict")["blocks"]

        paragraph_buffer = ""

        for block in blocks:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    cleaned_lines = clean_text(text)
                    for cline in cleaned_lines:
                        level = classify_heading_level(cline, span["size"])

                        if level > 0:  # Heading
                            if paragraph_buffer:
                                paragraph = {"type": "paragraph", "text": paragraph_buffer.strip()}
                                if section_stack:
                                    section_stack[-1]["content"].append(paragraph)
                                else:
                                    page_data["content"].append(paragraph)
                                paragraph_buffer = ""

                            if level == 1:
                                section = {"type": "section", "title": cline, "content": []}
                                page_data["content"].append(section)
                                section_stack = [section]

                            elif level == 2:
                                subsection = {"type": "subsection", "title": cline, "content": []}
                                if section_stack:
                                    section_stack[0]["content"].append(subsection)
                                    section_stack = [section_stack[0], subsection]
                                else:
                                    page_data["content"].append(subsection)
                                    section_stack = [subsection]
                        else:
                            paragraph_buffer += " " + cline

        if paragraph_buffer:
            paragraph = {"type": "paragraph", "text": paragraph_buffer.strip()}
            if section_stack:
                section_stack[-1]["content"].append(paragraph)
            else:
                page_data["content"].append(paragraph)

        # 🔹 Merge consecutive headings before saving
        page_data["content"] = merge_headings(page_data["content"])

        all_pages.append(page_data)

    return all_pages

# --------------------------
# Extract tables using pdfplumber
# --------------------------
def extract_tables(pdf_path):
    tables_by_page = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            if tables:
                tables_by_page[page_number] = tables
    return tables_by_page

# --------------------------
# Merge tables into hierarchical JSON
# --------------------------
def merge_tables_into_hierarchy(text_data, table_data):
    for page in text_data:
        page_number = page["page_number"]
        if page_number in table_data:
            for table in table_data[page_number]:
                table_block = {"type": "table", "text": table}
                # Add table to last section/subsection if exists
                if page["content"]:
                    last_block = page["content"][-1]
                    if last_block["type"] in ["section", "subsection"]:
                        last_block["content"].append(table_block)
                    else:
                        page["content"].append(table_block)
                else:
                    page["content"].append(table_block)
    return text_data

# --------------------------
# Save JSON
# --------------------------
def save_json(data, pdf_path):
    folder_path = os.path.dirname(pdf_path)
    json_path = os.path.join(folder_path, "parsed_output_hierarchical.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Hierarchical JSON created: {json_path}")

# --------------------------
# Run full extraction
# --------------------------
text_data = extract_hierarchical_text(file_path)
table_data = extract_tables(file_path)
final_data = merge_tables_into_hierarchy(text_data, table_data)
save_json(final_data, file_path)
