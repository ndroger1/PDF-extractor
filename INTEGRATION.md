# PDF Extractor + Remediator Integration

This extractor integrates seamlessly with the [PDF Remediator](https://github.com/adasheasu/pdfremediator) for complete PDF accessibility workflows.

## Complete Workflow

```
Extract → Analyze → Remediate → Verify
```

## Quick Integration

### Install Both Tools

```bash
# Clone repositories
git clone https://github.com/ndroger1/PDF-extractor.git
git clone https://github.com/adasheasu/pdfremediator.git

# Install dependencies
cd PDF-extractor
pip install -r requirements_extractor.txt

cd ../pdfremediator
pip install -r requirements.txt
```

### Use Integrated Workflow

```bash
# Option 1: All-in-one script (copy pdf_workflow.py to remediator directory)
python pdf_workflow.py input.pdf --output accessible.pdf --generate-report

# Option 2: Step-by-step
python pdf_extractor.py input.pdf --output data.json --extract-images
python pdf_remediator.py input.pdf --output accessible.pdf
```

## Integration Scripts

This repository includes integration scripts:

1. **`pdf_workflow.py`** - Complete workflow combining extraction, analysis, and remediation
2. **`examples/complete_workflow.py`** - Integration examples
3. **`WORKFLOW_GUIDE.md`** - Detailed integration guide
4. **`test_workflow.py`** - Test integration setup

## Use Cases

### 1. Pre-Remediation Analysis

```python
from pdf_extractor import PDFExtractor

# Extract to understand document structure
extractor = PDFExtractor("document.pdf", extract_images=True)
extraction = extractor.extract()

# Analyze findings
print(f"Found {extraction.total_images} images")
print(f"Found {extraction.total_words} words")

# Use this data to inform remediation strategy
```

### 2. Post-Remediation Verification

```bash
# Before
python pdf_extractor.py original.pdf --output before.json

# Remediate
python pdf_remediator.py original.pdf --output accessible.pdf

# After
python pdf_extractor.py accessible.pdf --output after.json

# Compare
python -c "
import json
before = json.load(open('before.json'))
after = json.load(open('after.json'))
print(f'Images: {before[\"total_images\"]} → {after[\"total_images\"]}')
"
```

### 3. Automated Pipeline

```python
from pdf_extractor import PDFExtractor
from pdf_workflow import PDFAccessibilityWorkflow

# Full automated pipeline
workflow = PDFAccessibilityWorkflow(
    pdf_path="document.pdf",
    output_path="accessible.pdf",
    generate_report=True
)

report, success = workflow.run()

if success:
    print(f"✓ Fixed {len(report.issues)} issues")
else:
    print("Manual intervention needed")
```

## Data Flow

```
PDF Document
     │
     ▼
[PDF Extractor]
  - Words with positions
  - Images with metadata
  - Document structure
     │
     ▼
[Accessibility Analyzer]
  - WCAG compliance check
  - Issue identification
  - Recommendations
     │
     ▼
[PDF Remediator]
  - Add tags
  - Add alt text
  - Fix reading order
  - Update metadata
     │
     ▼
Accessible PDF
```

## Installation for Integration

```bash
# All dependencies for both tools
pip install pikepdf PyMuPDF pdfplumber Pillow

# Optional: OCR
pip install pytesseract
# Also install Tesseract-OCR on your system

# Optional: AI alt text
pip install anthropic openid
```

## Documentation

- **[WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)** - Complete integration guide
- **[README.md](README.md)** - Extractor documentation
- **[QUICKSTART_EXTRACTOR.md](QUICKSTART_EXTRACTOR.md)** - Quick start

## Related Projects

- **PDF Remediator**: https://github.com/adasheasu/pdfremediator
- **PDF Extractor**: https://github.com/ndroger1/PDF-extractor

## Benefits of Integration

1. **Data-Driven Remediation** - Understand document structure before fixing
2. **Automated Analysis** - Identify accessibility issues automatically
3. **Verification** - Confirm improvements after remediation
4. **Batch Processing** - Process multiple PDFs consistently
5. **Custom Workflows** - Build your own accessibility pipelines

## Example: Complete Pipeline

```python
#!/usr/bin/env python3
"""Complete accessibility pipeline."""

from pathlib import Path
from pdf_extractor import PDFExtractor
from pdf_workflow import PDFAccessibilityWorkflow

def process_directory(input_dir, output_dir):
    """Process all PDFs in directory."""
    Path(output_dir).mkdir(exist_ok=True)

    for pdf_file in Path(input_dir).glob("*.pdf"):
        print(f"\nProcessing: {pdf_file.name}")

        # Run workflow
        output_file = Path(output_dir) / f"{pdf_file.stem}_accessible.pdf"
        workflow = PDFAccessibilityWorkflow(
            pdf_path=str(pdf_file),
            output_path=str(output_file),
            generate_report=True
        )

        report, success = workflow.run()

        if success:
            print(f"✓ {pdf_file.name}: Fixed {len(report.issues)} issues")
        else:
            print(f"✗ {pdf_file.name}: Failed")

if __name__ == "__main__":
    process_directory("input_pdfs", "accessible_pdfs")
```

## Support

For questions or issues:
- Extractor issues: https://github.com/ndroger1/PDF-extractor/issues
- Remediator issues: https://github.com/adasheasu/pdfremediator/issues
