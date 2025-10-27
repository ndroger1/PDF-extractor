#!/usr/bin/env python3
"""
PDF Extractor - Example Usage Demonstrations

This script demonstrates various ways to use the PDF extractor to read
every word and image from PDF documents.
"""

import sys
from pathlib import Path

# Add parent directory to path to import pdf_extractor
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_extractor import PDFExtractor, PDFExtraction


def example_1_basic_extraction():
    """Example 1: Basic extraction - get all words and text."""
    print("=" * 80)
    print("Example 1: Basic Text Extraction")
    print("=" * 80)

    # Replace with your PDF path
    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        print("Please provide a valid PDF path")
        return

    # Create extractor
    extractor = PDFExtractor(
        pdf_path=pdf_path,
        extract_images=False  # Only text for this example
    )

    # Extract content
    extraction = extractor.extract()

    # Display results
    print(f"\nExtracted {extraction.total_words} words from {extraction.num_pages} pages")

    # Show first page words
    if extraction.pages:
        first_page = extraction.pages[0]
        print(f"\nFirst 10 words from page 1:")
        for word in first_page.words[:10]:
            print(f"  '{word.text}' at ({word.x0:.1f}, {word.y0:.1f})")

    # Save to JSON
    extractor.save_to_json(extraction, "extraction_basic.json")
    print("\nFull results saved to: extraction_basic.json")


def example_2_with_images():
    """Example 2: Extract text and images."""
    print("\n" + "=" * 80)
    print("Example 2: Text + Image Extraction")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    # Create output directory for images
    images_dir = Path("extracted_images")

    # Create extractor
    extractor = PDFExtractor(
        pdf_path=pdf_path,
        extract_images=True,
        images_dir=str(images_dir)
    )

    # Extract content
    extraction = extractor.extract()

    # Display results
    print(f"\nExtracted:")
    print(f"  Words: {extraction.total_words}")
    print(f"  Images: {extraction.total_images}")

    # Show image details
    for page in extraction.pages:
        if page.images:
            print(f"\nPage {page.page_number} images:")
            for img in page.images:
                print(f"  - {img.name}: {img.width}x{img.height} ({img.format})")
                if img.file_path:
                    print(f"    Saved to: {img.file_path}")

    # Save results
    extractor.save_to_json(extraction, "extraction_with_images.json")
    print(f"\nImages saved to: {images_dir}")
    print("Full results saved to: extraction_with_images.json")


def example_3_with_ocr():
    """Example 3: Extract with OCR for scanned documents."""
    print("\n" + "=" * 80)
    print("Example 3: Extraction with OCR")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    try:
        # Create extractor with OCR enabled
        extractor = PDFExtractor(
            pdf_path=pdf_path,
            extract_images=True,
            images_dir="extracted_images_ocr",
            use_ocr=True  # Enable OCR
        )

        # Extract content
        extraction = extractor.extract()

        print(f"\nExtracted:")
        print(f"  Words: {extraction.total_words}")
        print(f"  Images: {extraction.total_images}")

        # Show OCR results
        for page in extraction.pages:
            for img in page.images:
                if img.ocr_text:
                    print(f"\nOCR from {img.name}:")
                    print(f"  {img.ocr_text[:200]}...")

        # Save results
        extractor.save_to_json(extraction, "extraction_with_ocr.json")
        print("\nFull results saved to: extraction_with_ocr.json")

    except Exception as e:
        print(f"Error: {e}")
        print("OCR requires pytesseract: pip install pytesseract")


def example_4_analyze_specific_page():
    """Example 4: Analyze a specific page in detail."""
    print("\n" + "=" * 80)
    print("Example 4: Detailed Page Analysis")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    extractor = PDFExtractor(pdf_path=pdf_path, extract_images=True)
    extraction = extractor.extract()

    # Analyze first page
    if extraction.pages:
        page = extraction.pages[0]

        print(f"\nPage 1 Analysis:")
        print(f"  Dimensions: {page.width:.1f} x {page.height:.1f}")
        print(f"  Rotation: {page.rotation}°")
        print(f"  Words: {page.word_count}")
        print(f"  Images: {page.image_count}")

        # Word statistics
        if page.words:
            font_sizes = [w.font_size for w in page.words if w.font_size > 0]
            if font_sizes:
                avg_font = sum(font_sizes) / len(font_sizes)
                print(f"\n  Average font size: {avg_font:.1f}")

            # Find largest words (likely headings)
            sorted_words = sorted(page.words, key=lambda w: w.font_size, reverse=True)
            print("\n  Largest words (likely headings):")
            for word in sorted_words[:5]:
                print(f"    '{word.text}' (size: {word.font_size:.1f})")

        # Image analysis
        if page.images:
            print(f"\n  Image details:")
            for img in page.images:
                print(f"    {img.name}:")
                print(f"      Size: {img.width}x{img.height}")
                print(f"      Position: ({img.x0:.1f}, {img.y0:.1f})")
                print(f"      Format: {img.format}")
                print(f"      File size: {img.size_bytes / 1024:.1f} KB")


def example_5_search_content():
    """Example 5: Search for specific text in PDF."""
    print("\n" + "=" * 80)
    print("Example 5: Search PDF Content")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    extractor = PDFExtractor(pdf_path=pdf_path)
    extraction = extractor.extract()

    # Search for a word
    search_term = "the"  # Change to your search term
    print(f"\nSearching for '{search_term}'...")

    matches = []
    for page in extraction.pages:
        for word in page.words:
            if search_term.lower() in word.text.lower():
                matches.append({
                    'page': page.page_number,
                    'text': word.text,
                    'position': (word.x0, word.y0)
                })

    print(f"\nFound {len(matches)} occurrences:")
    for i, match in enumerate(matches[:10], 1):  # Show first 10
        print(f"  {i}. Page {match['page']}: '{match['text']}' "
              f"at ({match['position'][0]:.1f}, {match['position'][1]:.1f})")

    if len(matches) > 10:
        print(f"  ... and {len(matches) - 10} more")


def example_6_text_report():
    """Example 6: Generate human-readable text report."""
    print("\n" + "=" * 80)
    print("Example 6: Generate Text Report")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    extractor = PDFExtractor(
        pdf_path=pdf_path,
        extract_images=True,
        images_dir="extracted_images_report"
    )

    extraction = extractor.extract()

    # Save as text report
    extractor.save_to_text(extraction, "extraction_report.txt")
    print("Text report saved to: extraction_report.txt")

    # Display a preview
    print("\nReport preview:")
    print("-" * 80)
    if extraction.pages:
        page = extraction.pages[0]
        preview = page.raw_text[:500] if page.raw_text else "No text"
        print(preview)
        if len(page.raw_text) > 500:
            print("...")
    print("-" * 80)


def main():
    """Run all examples."""
    print("PDF Extractor - Usage Examples")
    print("=" * 80)
    print()
    print("This script demonstrates various ways to use the PDF extractor.")
    print("Update the 'pdf_path' variable in each example to use your own PDF.")
    print()

    # Run examples
    examples = [
        ("Basic Extraction", example_1_basic_extraction),
        ("Extract Images", example_2_with_images),
        ("With OCR", example_3_with_ocr),
        ("Page Analysis", example_4_analyze_specific_page),
        ("Search Content", example_5_search_content),
        ("Text Report", example_6_text_report),
    ]

    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print()

    choice = input("Enter example number to run (or 'all' to run all): ").strip()

    if choice.lower() == 'all':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"Error in {name}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        name, func = examples[int(choice) - 1]
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
