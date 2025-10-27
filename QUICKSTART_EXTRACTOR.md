# Quick Start Guide - PDF Complete Extractor

## Installation (5 minutes)

### Step 1: Install Python Dependencies

```bash
cd pdfremediator
pip install -r requirements_extractor.txt
```

Or install individually:
```bash
pip install pikepdf PyMuPDF pdfplumber Pillow
```

### Step 2: (Optional) Install OCR Support

**Windows:**
- Download: https://github.com/UB-Mannheim/tesseract/wiki
- Run installer
- Install Python package: `pip install pytesseract`

**macOS:**
```bash
brew install tesseract
pip install pytesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
pip install pytesseract
```

## First Extraction (2 minutes)

### Command Line - Quick Test

```bash
# Basic extraction (text only)
python pdf_extractor.py your-document.pdf

# Save to JSON file
python pdf_extractor.py your-document.pdf --output results.json

# Extract images too
python pdf_extractor.py your-document.pdf --extract-images --images-dir ./images

# Everything with OCR
python pdf_extractor.py your-document.pdf --extract-images --ocr --output full_data.json
```

### Python Script - Quick Test

Create `test.py`:

```python
from pdf_extractor import PDFExtractor

# Create extractor
extractor = PDFExtractor(
    pdf_path="your-document.pdf",
    extract_images=True
)

# Extract everything
extraction = extractor.extract()

# Print summary
print(f"Extracted {extraction.total_words} words")
print(f"Extracted {extraction.total_images} images")

# Print first page words
page1 = extraction.pages[0]
for word in page1.words[:10]:
    print(f"'{word.text}' at ({word.x0:.0f}, {word.y0:.0f})")

# Save results
extractor.save_to_json(extraction, "output.json")
```

Run it:
```bash
python test.py
```

## Common Use Cases

### 1. Extract All Text
```bash
python pdf_extractor.py document.pdf --output text_data.json
```

Then access words:
```python
import json

with open('text_data.json') as f:
    data = json.load(f)

for page in data['pages']:
    for word in page['words']:
        print(f"{word['text']} at page {word['page']}")
```

### 2. Extract All Images
```bash
python pdf_extractor.py document.pdf \
  --extract-images \
  --images-dir ./extracted_images
```

Images are saved to `./extracted_images/` with names like `page1_img0.png`

### 3. Scanned PDF (with OCR)
```bash
python pdf_extractor.py scanned.pdf \
  --extract-images \
  --ocr \
  --output scanned_data.json
```

OCR text will be in the `ocr_text` field of each image.

### 4. Generate Report
```bash
python pdf_extractor.py document.pdf \
  --output report.txt \
  --format text
```

Creates a human-readable report with all content.

### 5. Search for Text
```python
from pdf_extractor import PDFExtractor

extractor = PDFExtractor("document.pdf")
extraction = extractor.extract()

# Search for a term
search_term = "invoice"
for page in extraction.pages:
    for word in page.words:
        if search_term.lower() in word.text.lower():
            print(f"Found on page {page.page_number}: {word.text}")
```

## Example Outputs

### JSON Output Structure
```json
{
  "total_words": 1523,
  "total_images": 4,
  "pages": [
    {
      "page_number": 1,
      "words": [
        {
          "text": "Invoice",
          "x0": 100.0,
          "y0": 700.0,
          "font_size": 24.0
        }
      ],
      "images": [
        {
          "name": "page1_img0",
          "width": 200,
          "height": 150,
          "format": "png"
        }
      ]
    }
  ]
}
```

### Text Report Output
```
PDF Extraction Report
================================================================================

File: document.pdf
Pages: 10
Total Words: 1523
Total Images: 4

================================================================================

PAGE 1
--------------------------------------------------------------------------------
Dimensions: 612.0 x 792.0
Words: 234
Images: 1

TEXT CONTENT:
Invoice
Date: 2024-01-15
Amount: $1,234.56
...
```

## Troubleshooting

### "pikepdf not found"
```bash
pip install pikepdf
```

### "No text extracted"
Install recommended libraries:
```bash
pip install PyMuPDF pdfplumber
```

### "OCR not working"
1. Install Tesseract-OCR on your system
2. Install Python package: `pip install pytesseract`

### Out of memory with large PDFs
- Don't use `--include-base64`
- Process in smaller batches
- Save images to disk instead of memory

## Next Steps

1. **Read the full documentation**: See `EXTRACTOR_README.md`
2. **Try the examples**: Run `python examples/extractor_demo.py`
3. **Integrate with your code**: Import `PDFExtractor` and customize

## Getting Help

- Check `EXTRACTOR_README.md` for detailed documentation
- Look at `examples/extractor_demo.py` for code examples
- Review `test_extractor.py` to verify your installation
- Check original PDF Remediator docs for integration

## Key Files

- `pdf_extractor.py` - Main extraction script
- `requirements_extractor.txt` - Python dependencies
- `EXTRACTOR_README.md` - Full documentation
- `examples/extractor_demo.py` - Usage examples
- `test_extractor.py` - Test/validation script
- `QUICKSTART_EXTRACTOR.md` - This file

## What You Can Extract

✅ Every word with exact positioning
✅ Every image with metadata
✅ Font information (name, size, style)
✅ Page dimensions and rotation
✅ PDF metadata (title, author, dates)
✅ OCR text from images
✅ Image positioning on pages
✅ Document structure

## Integration with PDF Remediator

The extractor works alongside the PDF Remediator:

```bash
# 1. Extract content
python pdf_extractor.py document.pdf --output analysis.json

# 2. Analyze for accessibility issues (use analysis.json)

# 3. Remediate with PDF Remediator
python pdf_remediator.py document.pdf --output accessible.pdf

# 4. Verify improvements
python pdf_extractor.py accessible.pdf --output verification.json
```

---

Happy extracting! 📄✨
