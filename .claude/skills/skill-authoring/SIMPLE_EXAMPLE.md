# Simple Example: PDF Processing Skill

This example demonstrates a well-structured Skill with progressive disclosure, proper organization, and clear patterns.

## Directory structure

```
pdf-processing/
├── SKILL.md (main instructions)
├── FORMS.md (form-filling guide)
├── REFERENCE.md (detailed API reference)
└── scripts/
    ├── analyze_form.py (extract form fields)
    ├── validate.py (validate field mappings)
    └── fill_form.py (fill PDF forms)
```

## SKILL.md

```markdown
---
name: PDF Processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

Process PDF files including text extraction, table parsing, form filling, and document merging.

## When to use this Skill

- Extracting text or tables from PDF files
- Filling out PDF forms programmatically
- Merging or splitting PDF documents
- Analyzing PDF structure and metadata

## Quick start

Extract text with pdfplumber:

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

## Text extraction

Use pdfplumber for reliable text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    # Extract from single page
    text = pdf.pages[0].extract_text()

    # Extract from all pages
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text()
```

**For scanned PDFs:** Use OCR with pdf2image and pytesseract:

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf")
text = pytesseract.image_to_string(images[0])
```

## Table extraction

Extract tables as structured data:

```python
import pdfplumber

with pdfplumber.open("report.pdf") as pdf:
    table = pdf.pages[0].extract_table()
    # Returns list of lists
    for row in table:
        print(row)
```

## Form filling

For PDF form filling, see the complete workflow in [FORMS.md](FORMS.md).

**Quick overview:**
1. Analyze form structure
2. Create field mapping
3. Validate mappings
4. Fill and save

## Document merging

Combine multiple PDFs:

```python
from pypdf import PdfMerger

merger = PdfMerger()
merger.append("doc1.pdf")
merger.append("doc2.pdf")
merger.write("combined.pdf")
merger.close()
```

## API reference

For complete API documentation including all extraction options, see [REFERENCE.md](REFERENCE.md).

## Common patterns

### Extract and save

```python
import pdfplumber

def extract_to_file(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"

    with open(output_path, "w") as f:
        f.write(text)

extract_to_file("input.pdf", "output.txt")
```

### Extract tables to CSV

```python
import pdfplumber
import csv

def tables_to_csv(pdf_path, output_path):
    with pdfplumber.open(pdf_path) as pdf:
        table = pdf.pages[0].extract_table()

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(table)

tables_to_csv("report.pdf", "data.csv")
```

## Tips for success

1. **Try pdfplumber first** for most text and table extraction tasks
2. **Use OCR for scanned PDFs** when text extraction returns empty
3. **Validate form fields** before filling to catch errors early
4. **Test on sample PDFs** before processing batches
```

## FORMS.md (referenced file)

```markdown
# PDF Form Filling Guide

Complete workflow for filling PDF forms programmatically.

## Overview

PDF forms contain interactive fields (text boxes, checkboxes, dropdowns) that can be filled programmatically. This guide uses a validation-first approach to ensure reliable results.

## Workflow

1. Analyze the form structure
2. Create field mapping file
3. Validate mapping
4. Fill the form
5. Verify output

## Step 1: Analyze form

Use the analyze script to extract form fields:

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

This creates a JSON file with all form fields and their properties:

```json
{
  "customer_name": {"type": "text", "required": true},
  "email": {"type": "text", "required": true},
  "agree_terms": {"type": "checkbox", "required": false}
}
```

## Step 2: Create mapping

Edit `fields.json` to add values:

```json
{
  "customer_name": {"type": "text", "value": "John Smith"},
  "email": {"type": "text", "value": "john@example.com"},
  "agree_terms": {"type": "checkbox", "value": true}
}
```

## Step 3: Validate

Run validation before filling:

```bash
python scripts/validate.py fields.json
```

Validation checks:
- All required fields have values
- Field types match expected types
- Checkbox values are boolean
- No unknown fields referenced

**Fix all validation errors before proceeding.**

## Step 4: Fill form

Run the fill script:

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```

## Step 5: Verify

Open the output PDF and verify:
- All fields contain correct values
- Formatting is preserved
- PDF opens without errors

## Troubleshooting

**Missing fields:** Re-run analyze_form.py to ensure all fields are detected

**Type errors:** Check that checkbox values are true/false, not "true"/"false"

**Required field errors:** Ensure all required fields have values in fields.json
```

## What makes this example good

### Strong metadata
- **Name:** Clear and descriptive (under 64 chars)
- **Description:** Includes what it does + when to use it + key terms

### Progressive disclosure
- **Level 1:** Metadata always loaded (~100 tokens)
- **Level 2:** SKILL.md loaded when triggered (~300 lines)
- **Level 3:** FORMS.md and REFERENCE.md loaded only when needed

### One level deep
- All files (FORMS.md, REFERENCE.md) link directly from SKILL.md
- No nested references (SKILL.md → file1.md → file2.md)

### Clear patterns
- Concrete code examples, not abstract explanations
- Template pattern for common operations
- Workflow pattern with clear steps

### Concise yet complete
- SKILL.md under 500 lines
- Assumes Claude knows Python and PDF concepts
- Detailed content in separate files

### Good organization
- Quick start at the top
- Common operations inline
- Advanced topics in referenced files
- Scripts in separate directory

### Validation workflow
- Step 3 validates before filling (prevents errors)
- Clear error messages guide fixes
- Reversible planning (can iterate on fields.json)

## How Claude uses this Skill

1. **User asks:** "Extract text from this PDF and save it to a file"
2. **Claude loads:** SKILL.md (sees quick start and extract pattern)
3. **Claude uses:** Text extraction code from SKILL.md
4. **Claude doesn't load:** FORMS.md or REFERENCE.md (not needed)

VS.

1. **User asks:** "Fill out this PDF form with customer data"
2. **Claude loads:** SKILL.md (sees form filling section)
3. **Claude reads:** "For PDF form filling, see [FORMS.md](FORMS.md)"
4. **Claude loads:** FORMS.md via bash Read
5. **Claude follows:** Complete workflow from FORMS.md
6. **Claude executes:** Scripts (analyze_form.py, validate.py, fill_form.py)

Only relevant content enters the context window.
