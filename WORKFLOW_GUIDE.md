# PDF Accessibility Workflow Guide

Complete guide for the integrated extraction and remediation workflow.

## Overview

This workflow combines two powerful tools:

1. **PDF Extractor** - Extracts every word and image with detailed positioning
2. **PDF Remediator** - Fixes accessibility issues for WCAG 2.2 Level AA compliance

Together, they provide a complete solution for PDF accessibility.

## The Workflow

```
┌─────────────────┐
│   Input PDF     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 1. EXTRACT      │ ← pdf_extractor.py
│  - All words    │
│  - All images   │
│  - Metadata     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. ANALYZE      │ ← pdf_workflow.py
│  - Find issues  │
│  - WCAG check   │
│  - Generate     │
│    report       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. REMEDIATE    │ ← pdf_remediator.py
│  - Add tags     │
│  - Alt text     │
│  - Fix order    │
│  - Metadata     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. VERIFY       │
│  - Re-extract   │
│  - Compare      │
│  - Report       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Accessible PDF  │
└─────────────────┘
```

## Quick Start

### Option 1: All-in-One (Recommended)

```bash
# Complete workflow in one command
python pdf_workflow.py input.pdf --output accessible.pdf --generate-report

# This will:
# 1. Extract all content
# 2. Analyze for issues
# 3. Remediate the PDF
# 4. Generate detailed report
# 5. Verify improvements
```

### Option 2: Step-by-Step

```bash
# Step 1: Extract content
python pdf_extractor.py input.pdf --output data.json --extract-images

# Step 2: Analyze (creates report)
python pdf_workflow.py input.pdf --analyze-only --generate-report

# Step 3: Remediate
python pdf_remediator.py input.pdf --output accessible.pdf

# Step 4: Verify
python pdf_extractor.py accessible.pdf --output verification.json
```

## Detailed Usage

### 1. Content Extraction

Extract every word and image from the PDF:

```bash
# Basic extraction
python pdf_extractor.py document.pdf

# Extract with images
python pdf_extractor.py document.pdf \
  --extract-images \
  --images-dir ./images \
  --output extraction.json

# With OCR for scanned documents
python pdf_extractor.py scanned.pdf \
  --extract-images \
  --ocr \
  --output data.json
```

**Python API:**

```python
from pdf_extractor import PDFExtractor

extractor = PDFExtractor(
    pdf_path="document.pdf",
    extract_images=True,
    images_dir="./images"
)

extraction = extractor.extract()

# Access data
print(f"Words: {extraction.total_words}")
print(f"Images: {extraction.total_images}")

# Each word has:
for word in extraction.pages[0].words:
    print(f"{word.text} at ({word.x0}, {word.y0})")
    print(f"  Font: {word.font_name} {word.font_size}pt")

# Each image has:
for img in extraction.pages[0].images:
    print(f"{img.name}: {img.width}x{img.height}")
```

### 2. Accessibility Analysis

Analyze the extracted content for WCAG issues:

```bash
# Analyze and generate report
python pdf_workflow.py document.pdf \
  --analyze-only \
  --generate-report

# This creates: document_accessibility_report.txt
```

**Python API:**

```python
from pdf_extractor import PDFExtractor
from pdf_workflow import PDFAccessibilityAnalyzer

# Extract first
extractor = PDFExtractor("document.pdf", extract_images=True)
extraction = extractor.extract()

# Analyze
analyzer = PDFAccessibilityAnalyzer(extraction)
report = analyzer.analyze()

print(f"Issues found: {len(report.issues)}")
print(f"Critical: {report.critical_count}")
print(f"High: {report.high_count}")

# Review issues
for issue in report.issues:
    print(f"\n{issue.issue_type} (Page {issue.page})")
    print(f"  Severity: {issue.severity}")
    print(f"  WCAG: {issue.wcag_criterion}")
    print(f"  Fix: {issue.recommendation}")
    print(f"  Auto-fixable: {issue.auto_fixable}")
```

### 3. Remediation

Fix the accessibility issues:

```bash
# Complete workflow (extract + analyze + remediate)
python pdf_workflow.py document.pdf \
  --output accessible.pdf \
  --generate-report

# Or use remediator directly
python pdf_remediator.py document.pdf \
  --output accessible.pdf
```

**The remediator fixes:**
- Missing document tags
- Images without alt text
- Incorrect reading order
- Missing metadata
- Heading structure
- Table structure
- Link descriptions

### 4. Verification

Verify improvements:

```bash
# Re-extract and analyze
python pdf_extractor.py accessible.pdf --output after.json
python pdf_workflow.py accessible.pdf --analyze-only
```

Compare before/after:

```python
# Load both reports
import json

with open('extraction_before.json') as f:
    before = json.load(f)

with open('extraction_after.json') as f:
    after = json.load(f)

# Compare
print(f"Images before: {before['total_images']}")
print(f"Images after: {after['total_images']}")
```

## Common Workflows

### Workflow 1: Single PDF Accessibility

```bash
# One command to rule them all
python pdf_workflow.py mydoc.pdf \
  --output mydoc_accessible.pdf \
  --generate-report

# Output:
# - mydoc_accessible.pdf (remediated PDF)
# - mydoc_accessibility_report.txt (detailed report)
# - mydoc_extraction.json (extraction data)
```

### Workflow 2: Batch Processing

```python
from pathlib import Path
from pdf_workflow import PDFAccessibilityWorkflow

pdf_dir = Path("pdfs")
output_dir = Path("accessible_pdfs")
output_dir.mkdir(exist_ok=True)

for pdf_file in pdf_dir.glob("*.pdf"):
    print(f"Processing {pdf_file.name}...")

    output_file = output_dir / f"{pdf_file.stem}_accessible.pdf"

    workflow = PDFAccessibilityWorkflow(
        pdf_path=str(pdf_file),
        output_path=str(output_file),
        generate_report=True
    )

    report, success = workflow.run()

    if success:
        print(f"✓ {pdf_file.name}: {len(report.issues)} issues fixed")
    else:
        print(f"✗ {pdf_file.name}: Failed")
```

### Workflow 3: Analysis Dashboard

```python
from pdf_extractor import PDFExtractor
from pdf_workflow import PDFAccessibilityAnalyzer
import json

# Analyze multiple PDFs
results = []

for pdf_file in Path("pdfs").glob("*.pdf"):
    extractor = PDFExtractor(str(pdf_file), extract_images=True)
    extraction = extractor.extract()

    analyzer = PDFAccessibilityAnalyzer(extraction)
    report = analyzer.analyze()

    results.append({
        'filename': pdf_file.name,
        'pages': extraction.num_pages,
        'words': extraction.total_words,
        'images': extraction.total_images,
        'issues_total': len(report.issues),
        'issues_critical': report.critical_count,
        'issues_high': report.high_count,
        'issues_medium': report.medium_count,
        'issues_low': report.low_count
    })

# Save dashboard data
with open('dashboard.json', 'w') as f:
    json.dump(results, f, indent=2)

# Print summary
print("\nAccessibility Dashboard")
print("=" * 80)
for r in results:
    print(f"{r['filename']}: {r['issues_total']} issues "
          f"({r['issues_critical']} critical)")
```

### Workflow 4: Custom Checks

```python
from pdf_extractor import PDFExtractor

extractor = PDFExtractor("document.pdf", extract_images=True)
extraction = extractor.extract()

# Custom check: Find all large text (potential headings)
potential_headings = []
for page in extraction.pages:
    for word in page.words:
        if word.font_size > 16:
            potential_headings.append({
                'page': page.page_number,
                'text': word.text,
                'size': word.font_size,
                'position': (word.x0, word.y0)
            })

print(f"Found {len(potential_headings)} potential headings")

# Custom check: Images by size
large_images = []
for page in extraction.pages:
    for img in page.images:
        if img.width > 200 and img.height > 200:
            large_images.append(img)

print(f"Found {len(large_images)} large images (>200x200)")
```

## Issue Types Detected

### Critical Issues
- **Images without alt text** (WCAG 1.1.1)
  - Auto-fixable with AI descriptions

### High Issues
- **Missing document title** (WCAG 2.4.2)
  - Auto-fixable from filename or content

- **Untagged headings** (WCAG 1.3.1)
  - Auto-fixable based on font size

### Medium Issues
- **Reading order problems** (WCAG 1.3.2)
  - Auto-fixable for simple layouts

- **Color contrast** (WCAG 1.4.3)
  - Requires manual verification

### Low Issues
- **Missing metadata** (Best practice)
  - Partially auto-fixable

## Configuration

### Using AI for Alt Text

```bash
# Set up API key
export ANTHROPIC_API_KEY="your-key"
# or
export OPENAI_API_KEY="your-key"

# Run with AI
python pdf_workflow.py document.pdf \
  --output accessible.pdf \
  --use-ai
```

### OCR for Scanned Documents

```bash
# Install Tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: apt-get install tesseract-ocr

pip install pytesseract

# Use OCR
python pdf_extractor.py scanned.pdf \
  --extract-images \
  --ocr \
  --output data.json
```

## Integration Patterns

### Pattern 1: Pre-flight Check

```python
# Check before processing
from pdf_workflow import PDFAccessibilityWorkflow

workflow = PDFAccessibilityWorkflow(
    pdf_path="document.pdf",
    output_path=None,  # No remediation
    generate_report=True
)

report, _ = workflow.run()

if report.critical_count > 0:
    print(f"❌ {report.critical_count} critical issues - manual review needed")
else:
    print("✓ Ready for automated remediation")
```

### Pattern 2: Progressive Enhancement

```python
# Fix critical issues first
def progressive_remediation(pdf_path):
    # Round 1: Auto-fix critical issues
    workflow = PDFAccessibilityWorkflow(pdf_path, "round1.pdf")
    report1, _ = workflow.run()

    # Round 2: Manual review if needed
    if report1.critical_count == 0:
        print("✓ All critical issues fixed")
        return "round1.pdf"
    else:
        print("⚠ Manual intervention required")
        return None
```

### Pattern 3: Quality Gate

```python
# Use in CI/CD pipeline
def accessibility_gate(pdf_path, max_critical=0, max_high=5):
    """Return True if PDF meets accessibility standards."""
    from pdf_extractor import PDFExtractor
    from pdf_workflow import PDFAccessibilityAnalyzer

    extractor = PDFExtractor(pdf_path, extract_images=True)
    extraction = extractor.extract()

    analyzer = PDFAccessibilityAnalyzer(extraction)
    report = analyzer.analyze()

    passed = (
        report.critical_count <= max_critical and
        report.high_count <= max_high
    )

    return passed, report

# Use in pipeline
passed, report = accessibility_gate("output.pdf")
if not passed:
    print(f"❌ Failed: {report.critical_count} critical, "
          f"{report.high_count} high issues")
    sys.exit(1)
```

## Troubleshooting

### No extraction data
```bash
# Check dependencies
pip install PyMuPDF pdfplumber

# Verify installation
python test_extractor.py
```

### Remediation fails
```bash
# Check pikepdf installation
pip install pikepdf

# Run remediator separately
python pdf_remediator.py input.pdf --output test.pdf
```

### Large PDFs
```bash
# Process pages in batches
python pdf_extractor.py large.pdf --output data.json
# Don't use --include-base64 for large PDFs
```

## Best Practices

1. **Always extract first** - Understand the document before remediating
2. **Review reports** - Some issues need manual attention
3. **Test with screen readers** - Automated fixes aren't perfect
4. **Verify results** - Re-analyze after remediation
5. **Use AI wisely** - AI alt text is better than nothing, but review it
6. **Keep originals** - Always work on copies
7. **Document decisions** - Note manual fixes in reports

## Output Files

The workflow generates:

```
document.pdf                           # Original
document_extraction.json               # Extraction data
document_accessibility_report.txt      # Analysis report
document_accessible.pdf                # Remediated PDF
document_accessible_extraction.json    # Verification data
```

## Next Steps

- Review `examples/complete_workflow.py` for code examples
- Check `pdf_workflow.py` for the main workflow script
- See `pdf_extractor.py` for extraction details
- Read `pdf_remediator.py` for remediation options

## Support

For issues or questions:
- Extractor: https://github.com/ndroger1/PDF-extractor
- Remediator: https://github.com/adasheasu/pdfremediator
