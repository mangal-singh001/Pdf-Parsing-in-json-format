# PDF Parsing to Structured JSON

Extract text from a PDF and convert it into a well-structured JSON format.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Folder Structure](#folder-structure)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [JSON Output Format](#json-output-format)
* [Example](#example)
* [Limitations & Future Work](#limitations--future-work)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

This project allows you to input a PDF file, parse its contents, and output a **hierarchical / structured JSON** representation of the text and layout structure. Instead of dumping all text in a flat stream, the output groups content meaningfully (e.g. pages, paragraphs, headings, sections).

The goal is to get machine-friendly structured data from arbitrary PDFs, useful for indexing, data extraction, or downstream processing.

---

## Features

* Parse multi-page PDFs
* Preserve page boundaries
* Group text into blocks / paragraphs
* Optionally detect headings / sections (if heuristics are available)
* Output clean, readable JSON structure
* Works with standard PDF libraries in Python

---

## Folder Structure

```text
Pdf-Parsing-in-json-format/
├── Assignment Task_ PDF Parsing.pdf
├── PDF Parsing and Structured JSON.py
├── [Fund Factsheet - May]360ONE-MF-May 2025.pdf.pdf
├── parsed_output_hierarchical.json
└── README.md
```

* `PDF Parsing and Structured JSON.py` — main script for parsing
* `parsed_output_hierarchical.json` — sample output
* Example input PDFs included for testing

---

## Requirements

* Python 3.7+
* PDF parsing library (e.g. `PyPDF2`, `pdfminer.six`, `pdfplumber`)
* (Optional) Additional NLP / text layout heuristics

You can install dependencies (if any) via:

```bash
pip install pdfminer.six
# or
pip install pdfplumber
```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mangal-singh001/Pdf-Parsing-in-json-format.git
   cd Pdf-Parsing-in-json-format
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate     # on Linux / macOS
   venv\Scripts\activate        # on Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   *If there’s no `requirements.txt`, manually ensure you have the PDF parsing library installed.*

---

## Usage

Run the script with an input PDF file and optionally an output JSON path. Example:

```bash
python "PDF Parsing and Structured JSON.py" input.pdf output.json
```

If the script doesn’t accept command-line arguments, you can modify it to open a PDF file and write to JSON. For instance:

```python
from pdf_parser import parse_pdf_to_json

json_obj = parse_pdf_to_json("input.pdf")
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(json_obj, f, ensure_ascii=False, indent=2)
```

---

## JSON Output Format

Below is a suggested structure for how the JSON could be organized. You may adjust this based on your script’s output.

```json
{
  "filename": "input.pdf",
  "num_pages": 3,
  "pages": [
    {
      "page_number": 1,
      "height": 792,
      "width": 612,
      "blocks": [
        {
          "type": "paragraph",
          "text": "This is the first paragraph on page 1.",
          "bbox": [x0, y0, x1, y1]
        },
        {
          "type": "heading",
          "text": "Section 1: Introduction",
          "bbox": [...]
        }
      ]
    },
    {
      "page_number": 2,
      "blocks": [
        ...
      ]
    }
  ]
}
```

* **filename**: name of the input PDF
* **num_pages**: total pages
* **pages**: array of page objects

  * Each page may include dimensions, blocks
  * **blocks**: each block may be a paragraph, heading, table, etc.
  * **bbox**: bounding box / coordinates (optional)
  * **text**: the extracted text

You can enrich this further (e.g. include font size, style, whitespace info).

---

## Example

Given an input file `sample.pdf`, the output might look like:

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
          "text": "Overview",
          "bbox": [50, 700, 500, 730]
        },
        {
          "type": "paragraph",
          "text": "This document describes ...",
          "bbox": [50, 650, 500, 690]
        }
      ]
    },
    {
      "page_number": 2,
      "blocks": [
        {
          "type": "paragraph",
          "text": "Further details are ...",
          "bbox": [50, 650, 500, 710]
        }
      ]
    }
  ]
}
```

You can view already included sample output in `parsed_output_hierarchical.json` in this repo.

---

## Limitations & Future Work

* Complex layouts (multi-column, images, tables) may not be handled well
* No OCR support (only works on text-based PDFs)
* Heuristics for section / heading detection may be brittle
* No styling metadata (fonts, colors) currently
* Future enhancements:

  * Add table detection & cell structure
  * Integrate OCR for scanned PDFs
  * Improve heading / section detection (using font size, spacing)
  * Allow custom JSON schemas or templates

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Make your changes & add tests
4. Commit & push
5. Open a pull request

Please follow PEP 8, write documentation, and test on multiple PDFs.

---

