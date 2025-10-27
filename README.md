# PDF Complete Extractor

A comprehensive tool to extract **every word** and **every image** from PDF documents with detailed positioning, formatting, and metadata.

## Features

- **Complete Word Extraction**: Extract every word with:
  - Exact positioning (x, y coordinates)
  - Font information (name, size, style)
  - Page number and dimensions

- **Complete Image Extraction**: Extract all images with:
  - Full metadata (dimensions, format, color space)
  - Positioning on page
  - Optional save to files
  - Optional base64 encoding
  - OCR text extraction (optional)

- **Multiple Output Formats**:
  - Structured JSON with all details
  - Human-readable text reports
  - CSV export (coming soon)

- **Flexible Processing**:
  - Page-by-page extraction
  - OCR support for scanned documents
  - AI-powered image analysis (optional)
  - Search and filter capabilities

## 🔗 Integration with PDF Remediator

This extractor integrates with [PDF Remediator](https://github.com/adasheasu/pdfremediator) for a **complete PDF accessibility workflow**:

```
Extract → Analyze → Remediate → Verify
```

**Quick integration:**
```bash
# Complete workflow in one command
python pdf_workflow.py input.pdf --output accessible.pdf --generate-report
```

See [INTEGRATION.md](INTEGRATION.md) for full integration guide or [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) for detailed workflows.

## Installation

### Required Dependencies

```bash
pip install pikepdf
```

### Recommended Dependencies (for best results)

```bash
pip install PyMuPDF pdfplumber Pillow
```

Or install all at once:

```bash
pip install -r requirements_extractor.txt
```

### Optional: OCR Support

For OCR functionality, install Tesseract-OCR and pytesseract:

**Windows:**
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install pytesseract: `pip install pytesseract`

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

## Quick Start

### Command Line Usage

```bash
# Basic extraction to JSON
python pdf_extractor.py document.pdf --output data.json

# Extract with images saved to directory
python pdf_extractor.py document.pdf --extract-images --images-dir ./images

# Include OCR for images
python pdf_extractor.py document.pdf --ocr --extract-images

# Generate human-readable text report
python pdf_extractor.py document.pdf --output report.txt --format text

# Include base64 image data in JSON
python pdf_extractor.py document.pdf --output data.json --include-base64
```

### Python API Usage

```python
from pdf_extractor import PDFExtractor

# Create extractor
extractor = PDFExtractor(
    pdf_path="document.pdf",
    extract_images=True,
    images_dir="./extracted_images"
)

# Extract all content
extraction = extractor.extract()

# Access data
print(f"Total words: {extraction.total_words}")
print(f"Total images: {extraction.total_images}")

# Access page data
for page in extraction.pages:
    print(f"\nPage {page.page_number}:")
    print(f"  Words: {page.word_count}")
    print(f"  Images: {page.image_count}")

    # Access individual words
    for word in page.words[:5]:  # First 5 words
        print(f"  '{word.text}' at ({word.x0}, {word.y0})")

    # Access images
    for img in page.images:
        print(f"  Image: {img.width}x{img.height} {img.format}")

# Save results
extractor.save_to_json(extraction, "output.json")
extractor.save_to_text(extraction, "output.txt")
```

## Usage Examples

See `examples/extractor_demo.py` for comprehensive examples including:

1. **Basic text extraction** - Get all words with positioning
2. **Image extraction** - Extract and save all images
3. **OCR extraction** - Extract text from images in scanned PDFs
4. **Page analysis** - Detailed analysis of specific pages
5. **Content search** - Search for text across the document
6. **Report generation** - Create formatted text reports

Run the demo:
```bash
python examples/extractor_demo.py
```

## Output Format

### JSON Structure

```json
{
  "file_path": "document.pdf",
  "num_pages": 10,
  "total_words": 5432,
  "total_images": 15,
  "title": "Document Title",
  "author": "Author Name",
  "pages": [
    {
      "page_number": 1,
      "width": 612.0,
      "height": 792.0,
      "word_count": 543,
      "image_count": 2,
      "words": [
        {
          "text": "Hello",
          "page": 1,
          "x0": 72.0,
          "y0": 720.0,
          "x1": 110.5,
          "y1": 732.0,
          "font_name": "Arial-Bold",
          "font_size": 12.0
        }
      ],
      "images": [
        {
          "page": 1,
          "name": "page1_img0",
          "width": 400,
          "height": 300,
          "format": "png",
          "x0": 100.0,
          "y0": 400.0,
          "file_path": "./images/page1_img0.png",
          "ocr_text": "Text found in image"
        }
      ]
    }
  ]
}
```

## Word Data Fields

Each word includes:
- `text`: The word text
- `page`: Page number (1-indexed)
- `x0, y0`: Top-left corner coordinates
- `x1, y1`: Bottom-right corner coordinates
- `width, height`: Word dimensions
- `font_name`: Font family name
- `font_size`: Font size in points
- `is_bold`: Bold formatting (if detected)
- `is_italic`: Italic formatting (if detected)

## Image Data Fields

Each image includes:
- `page`: Page number
- `name`: Unique image identifier
- `width, height`: Image dimensions in pixels
- `x0, y0, x1, y1`: Position on page
- `format`: Image format (png, jpg, etc.)
- `size_bytes`: File size in bytes
- `color_space`: Color space information
- `file_path`: Path to saved image file (if saved)
- `base64_data`: Base64 encoded image (if requested)
- `ocr_text`: Extracted text from image (if OCR enabled)

## Command Line Options

```
usage: pdf_extractor.py [-h] [-o OUTPUT] [--format {json,text}]
                       [--extract-images] [--images-dir IMAGES_DIR]
                       [--ocr] [--include-base64] [--ai-analysis]
                       pdf_path

positional arguments:
  pdf_path              Path to PDF file

optional arguments:
  -h, --help            Show help message
  -o, --output OUTPUT   Output file path
  --format {json,text}  Output format (default: json)
  --extract-images      Extract images from PDF
  --images-dir DIR      Directory to save extracted images
  --ocr                 Use OCR on images (requires pytesseract)
  --include-base64      Include base64 encoded image data in JSON
  --ai-analysis         Use AI for image description (requires AI integration)
```

## Use Cases

### 1. Document Analysis
Extract and analyze all text to understand document structure, identify headings, and map content flow.

### 2. Data Mining
Extract specific information by searching through all words with their context and positioning.

### 3. Accessibility
Identify images needing alt text and extract their visual content for description.

### 4. Content Migration
Extract complete content for migration to other formats or systems.

### 5. Scanned Document Processing
Use OCR to extract text from image-based PDFs.

### 6. Document Comparison
Compare documents by analyzing word-by-word differences.

### 7. Layout Analysis
Analyze document layout by examining word and image positions.

## Performance Notes

- **pdfplumber + PyMuPDF** (recommended): Best extraction quality for both text and images
- **pdfplumber only**: Good text extraction, limited image support
- **PyMuPDF only**: Good for both text and images, slightly different text format
- **pikepdf only**: Limited extraction capabilities (fallback)

### Processing Speed

Approximate processing times (varies by document complexity):
- Text-only: ~1-2 seconds per page
- With images: ~2-5 seconds per page
- With OCR: ~5-15 seconds per page (depends on image count/size)

## Integration with PDF Remediator

This extractor complements the PDF Remediator tool:

1. **Extract**: Use `pdf_extractor.py` to get all content
2. **Analyze**: Review extracted data to identify accessibility issues
3. **Remediate**: Use `pdf_remediator.py` to fix issues
4. **Verify**: Extract again to verify improvements

## Troubleshooting

### "Module not found" errors
Install required dependencies:
```bash
pip install PyMuPDF pdfplumber
```

### OCR not working
1. Ensure Tesseract-OCR is installed on your system
2. Install pytesseract: `pip install pytesseract`
3. On Windows, you may need to add Tesseract to PATH

### Images not extracting
- Install PyMuPDF: `pip install PyMuPDF`
- Install Pillow: `pip install Pillow`

### Memory issues with large PDFs
- Process pages in batches
- Don't use `--include-base64` for large image-heavy PDFs
- Save images to disk instead of keeping in memory

## Contributing

Contributions welcome! Areas for enhancement:
- CSV export format
- Enhanced AI image analysis integration
- Table detection and extraction
- Form field extraction
- Annotation extraction
- Multi-threaded processing for large documents

## License

Same license as the parent PDF Remediator project.

## Credits

Built as an extension to the [PDF Remediator](https://github.com/adasheasu/pdfremediator) project.

Uses:
- [pikepdf](https://github.com/pikepdf/pikepdf) - PDF manipulation
- [PyMuPDF](https://pymupdf.readthedocs.io/) - Image and text extraction
- [pdfplumber](https://github.com/jsvine/pdfplumber) - Word-level text extraction
- [pytesseract](https://github.com/madmaze/pytesseract) - OCR support
