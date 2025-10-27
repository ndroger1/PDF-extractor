#!/usr/bin/env python3
"""
Test script for PDF Extractor

This script validates the PDF extractor functionality.
Run with a sample PDF to test extraction capabilities.
"""

import sys
from pathlib import Path
import json

# Test imports
print("Testing imports...")
try:
    from pdf_extractor import PDFExtractor, PDFExtraction, WordInfo, ImageData, PageData
    print("✓ Core extractor modules imported successfully")
except ImportError as e:
    print(f"✗ Failed to import extractor: {e}")
    sys.exit(1)

try:
    import pikepdf
    print("✓ pikepdf installed")
except ImportError:
    print("✗ pikepdf not installed (required)")
    print("  Install: pip install pikepdf")

try:
    import PyMuPDF
    print("✓ PyMuPDF installed (recommended)")
except ImportError:
    print("⚠ PyMuPDF not installed (recommended for best results)")
    print("  Install: pip install PyMuPDF")

try:
    import pdfplumber
    print("✓ pdfplumber installed (recommended)")
except ImportError:
    print("⚠ pdfplumber not installed (recommended for best results)")
    print("  Install: pip install pdfplumber")

try:
    from PIL import Image
    print("✓ Pillow installed")
except ImportError:
    print("⚠ Pillow not installed (optional)")
    print("  Install: pip install Pillow")

try:
    import pytesseract
    print("✓ pytesseract installed (optional for OCR)")
except ImportError:
    print("⚠ pytesseract not installed (optional for OCR)")
    print("  Install: pip install pytesseract")

print("\n" + "=" * 80)
print("Testing Data Classes")
print("=" * 80)

# Test data classes
try:
    word = WordInfo(
        text="test",
        page=1,
        x0=10.0,
        y0=20.0,
        x1=50.0,
        y1=35.0,
        width=40.0,
        height=15.0,
        font_name="Arial",
        font_size=12.0
    )
    print(f"✓ WordInfo created: '{word.text}' at ({word.x0}, {word.y0})")

    image = ImageData(
        page=1,
        index=0,
        name="test_img",
        width=100,
        height=100,
        x0=0, y0=0, x1=100, y1=100
    )
    print(f"✓ ImageData created: {image.name} ({image.width}x{image.height})")

    page = PageData(
        page_number=1,
        width=612.0,
        height=792.0,
        rotation=0,
        word_count=0,
        image_count=0
    )
    print(f"✓ PageData created: Page {page.page_number} ({page.width}x{page.height})")

    extraction = PDFExtraction(
        file_path="test.pdf",
        file_size=1024,
        num_pages=1
    )
    print(f"✓ PDFExtraction created: {extraction.num_pages} pages")

except Exception as e:
    print(f"✗ Data class error: {e}")

print("\n" + "=" * 80)
print("Testing JSON Serialization")
print("=" * 80)

try:
    # Test serialization
    word_dict = word.to_dict()
    json_str = json.dumps(word_dict, indent=2)
    print(f"✓ Word serialization works")
    print(f"  Sample: {json_str[:100]}...")

    extraction.pages.append(page)
    page.words.append(word)
    page.images.append(image)
    page.word_count = 1
    page.image_count = 1

    extraction_dict = extraction.to_dict()
    json_str = json.dumps(extraction_dict, indent=2)
    print(f"✓ Full extraction serialization works")
    print(f"  Size: {len(json_str)} characters")

except Exception as e:
    print(f"✗ Serialization error: {e}")

print("\n" + "=" * 80)
print("Ready for PDF Testing")
print("=" * 80)
print()
print("To test with a real PDF, run:")
print()
print("  python pdf_extractor.py <your-pdf-file.pdf> --output test_output.json")
print()
print("Or use the example script:")
print()
print("  python examples/extractor_demo.py")
print()
print("Make sure to update the PDF path in the example script!")
print()
print("=" * 80)

# If a PDF path is provided as argument, test extraction
if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
    print(f"\nTesting extraction on: {pdf_path}")

    if not Path(pdf_path).exists():
        print(f"✗ PDF file not found: {pdf_path}")
        sys.exit(1)

    try:
        print("Creating extractor...")
        extractor = PDFExtractor(
            pdf_path=pdf_path,
            extract_images=True,
            images_dir="test_extraction_images"
        )
        print("✓ Extractor created")

        print("Extracting content...")
        extraction = extractor.extract()
        print("✓ Extraction completed")

        print(f"\nResults:")
        print(f"  Pages: {extraction.num_pages}")
        print(f"  Total words: {extraction.total_words}")
        print(f"  Total images: {extraction.total_images}")

        if extraction.pages:
            page = extraction.pages[0]
            print(f"\nFirst page:")
            print(f"  Dimensions: {page.width}x{page.height}")
            print(f"  Words: {page.word_count}")
            print(f"  Images: {page.image_count}")

            if page.words:
                print(f"\n  First 5 words:")
                for word in page.words[:5]:
                    print(f"    '{word.text}' at ({word.x0:.1f}, {word.y0:.1f})")

            if page.images:
                print(f"\n  Images:")
                for img in page.images:
                    print(f"    {img.name}: {img.width}x{img.height} ({img.format})")

        # Save test output
        output_path = "test_extraction.json"
        extractor.save_to_json(extraction, output_path)
        print(f"\n✓ Test results saved to: {output_path}")

        print("\n" + "=" * 80)
        print("TEST PASSED")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
else:
    print("\nTo test with your own PDF, run:")
    print(f"  python {Path(__file__).name} <your-pdf-file.pdf>")
