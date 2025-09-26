# 📄 PDF Parsing to Structured JSON

Extract text from a PDF 📑 and convert it into a **well-structured JSON** 🗂️ format.

---

## 📌 Table of Contents

* [✨ Overview](#-overview)
* [⚡ Features](#-features)
* [📂 Folder Structure](#-folder-structure)
* [🛠️ Requirements](#️-requirements)
* [⚙️ Installation](#-installation)
* [▶️ Usage](#️-usage)
* [📊 JSON Output Format](#-json-output-format)
* [📝 Example](#-example)
* [🔮 Limitations & Future Work](#-limitations--future-work)
* [🤝 Contributing](#-contributing)
* [📜 License](#-license)

---

## ✨ Overview

This project lets you **parse any PDF** and convert it into a **hierarchical JSON structure**.
Instead of dumping all the text, it groups the content into **pages, sections, and paragraphs**, making it easy to process further 🔍.

---

## ⚡ Features

✔️ Parse multi-page PDFs
✔️ Preserve page numbers
✔️ Group text into blocks / paragraphs
✔️ Optional heading / section detection
✔️ Clean & readable JSON output

---

## 📂 Folder Structure

```
Pdf-Parsing-in-json-format/
├── Assignment Task_ PDF Parsing.pdf
├── PDF Parsing and Structured JSON.py
├── [Fund Factsheet - May]360ONE-MF-May 2025.pdf.pdf
├── parsed_output_hierarchical.json
└── README.md
```

---

## 🛠️ Requirements

* Python 3.7+ 🐍
* PDF libraries (`pdfminer.six` or `pdfplumber`)
* JSON library (built-in)

Install dependencies:

```bash
pip install pdfminer.six
# or
pip install pdfplumber
```

---

## ⚙️ Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/mangal-singh001/Pdf-Parsing-in-json-format.git
   cd Pdf-Parsing-in-json-format
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS  
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the script with an input PDF and optional output JSON:

```bash
python "PDF Parsing and Structured JSON.py" input.pdf output.json
```

Example in Python:

```python
from pdf_parser import parse_pdf_to_json
import json

json_obj = parse_pdf_to_json("input.pdf")
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=2)
```

---

## 📊 JSON Output Format

Example JSON structure:

```json
{
  "filename": "sample.pdf",
  "num_pages": 2,
  "pages": [
    {
      "page_number": 1,
      "blocks": [
        {
          "type": "heading",
          "text": "Overview"
        },
        {
          "type": "paragraph",
          "text": "This document describes ..."
        }
      ]
    }
  ]
}
```

---

## 📝 Example

Input: **sample.pdf**
Output: **parsed_output_hierarchical.json**

```json
{
  "filename": "sample.pdf",
  "num_pages": 2,
  "pages": [
    {
      "page_number": 1,
      "blocks": [
        { "type": "heading", "text": "Overview" },
        { "type": "paragraph", "text": "This document describes ..." }
      ]
    }
  ]
}
```

---

## 🔮 Limitations & Future Work

⚠️ Current Limitations:

* No OCR (works only on text-based PDFs)
* Limited handling of tables & images
* Heading detection is heuristic-based

✨ Future Enhancements:

* OCR support for scanned PDFs 🖼️
* Table & chart extraction 📊
* Better heading/section classification

---

## 🤝 Contributing

Want to improve this project? 🙌

1. Fork the repo
2. Create a branch (`git checkout -b feature-name`)
3. Commit changes
4. Push & open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** ✅

---
