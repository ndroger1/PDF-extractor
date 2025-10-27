#!/usr/bin/env python3
"""
Complete PDF Accessibility Workflow Examples

Demonstrates the integrated workflow from extraction through remediation.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pdf_extractor import PDFExtractor
from pdf_workflow import PDFAccessibilityWorkflow


def example_1_basic_workflow():
    """Example 1: Basic workflow - analyze and remediate."""
    print("=" * 80)
    print("Example 1: Basic Workflow")
    print("=" * 80)

    pdf_path = "sample.pdf"  # Replace with your PDF

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    # Run complete workflow
    workflow = PDFAccessibilityWorkflow(
        pdf_path=pdf_path,
        output_path="sample_accessible.pdf",
        generate_report=True
    )

    report, success = workflow.run()

    if success:
        print("\n✓ Workflow completed successfully!")
        print(f"  Original: {pdf_path}")
        print(f"  Accessible: sample_accessible.pdf")
        print(f"  Report: {Path(pdf_path).stem}_accessibility_report.txt")


def example_2_analysis_only():
    """Example 2: Analyze PDF without remediation."""
    print("\n" + "=" * 80)
    print("Example 2: Analysis Only")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    # Step 1: Extract
    print("\nExtracting content...")
    extractor = PDFExtractor(pdf_path=pdf_path, extract_images=True)
    extraction = extractor.extract()

    print(f"Extracted:")
    print(f"  Pages: {extraction.num_pages}")
    print(f"  Words: {extraction.total_words}")
    print(f"  Images: {extraction.total_images}")

    # Step 2: Analyze
    print("\nAnalyzing accessibility...")
    from pdf_workflow import PDFAccessibilityAnalyzer

    analyzer = PDFAccessibilityAnalyzer(extraction)
    report = analyzer.analyze()

    print(f"\nAccessibility Issues:")
    print(f"  Critical: {report.critical_count}")
    print(f"  High: {report.high_count}")
    print(f"  Medium: {report.medium_count}")
    print(f"  Low: {report.low_count}")

    # Show issues
    print("\nTop Issues:")
    for issue in report.issues[:5]:
        print(f"\n  {issue.issue_type} (Page {issue.page})")
        print(f"    {issue.description}")
        print(f"    Fix: {issue.recommendation}")


def example_3_step_by_step():
    """Example 3: Step-by-step manual workflow."""
    print("\n" + "=" * 80)
    print("Example 3: Step-by-Step Workflow")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    # Step 1: Extract and save data
    print("\nStep 1: Extract PDF content")
    print("-" * 40)
    extractor = PDFExtractor(pdf_path=pdf_path, extract_images=True)
    extraction = extractor.extract()
    extractor.save_to_json(extraction, "extraction_data.json")
    print("✓ Content extracted and saved to extraction_data.json")

    # Step 2: Analyze issues
    print("\nStep 2: Analyze accessibility")
    print("-" * 40)
    from pdf_workflow import PDFAccessibilityAnalyzer

    analyzer = PDFAccessibilityAnalyzer(extraction)
    report = analyzer.analyze()
    print(f"✓ Found {len(report.issues)} issues")

    # Step 3: Review issues by type
    print("\nStep 3: Review issues by type")
    print("-" * 40)

    issues_by_type = {}
    for issue in report.issues:
        if issue.issue_type not in issues_by_type:
            issues_by_type[issue.issue_type] = []
        issues_by_type[issue.issue_type].append(issue)

    for issue_type, issues in issues_by_type.items():
        print(f"\n{issue_type}: {len(issues)} issues")
        for issue in issues[:2]:  # Show first 2
            print(f"  Page {issue.page}: {issue.description}")

    # Step 4: Generate report
    print("\nStep 4: Generate detailed report")
    print("-" * 40)
    report_text = report.get_summary()
    with open("accessibility_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
    print("✓ Report saved to accessibility_report.txt")

    # Step 5: Remediate (would be done with remediator)
    print("\nStep 5: Remediate PDF")
    print("-" * 40)
    print("Use pdf_remediator.py or pdf_workflow.py with --output option")
    print(f"  python pdf_workflow.py {pdf_path} --output accessible.pdf")


def example_4_custom_analysis():
    """Example 4: Custom analysis with extraction data."""
    print("\n" + "=" * 80)
    print("Example 4: Custom Analysis")
    print("=" * 80)

    pdf_path = "sample.pdf"

    if not Path(pdf_path).exists():
        print(f"Sample PDF not found: {pdf_path}")
        return

    extractor = PDFExtractor(pdf_path=pdf_path, extract_images=True)
    extraction = extractor.extract()

    # Custom analysis: Check for specific issues
    print("\nCustom Accessibility Checks:")
    print("-" * 40)

    # Check 1: Images without alt text
    images_needing_alt = 0
    for page in extraction.pages:
        for img in page.images:
            # Not decorative and no OCR text
            if img.width > 50 and img.height > 50 and not img.ocr_text:
                images_needing_alt += 1

    print(f"✓ Images needing alt text: {images_needing_alt}")

    # Check 2: Potential heading text
    potential_headings = []
    for page in extraction.pages:
        for word in page.words:
            if word.font_size > 16:
                potential_headings.append((page.page_number, word.text, word.font_size))

    print(f"✓ Potential headings found: {len(potential_headings)}")
    if potential_headings:
        print("\n  Sample headings:")
        for page, text, size in potential_headings[:3]:
            print(f"    Page {page}: '{text}' (size {size:.1f})")

    # Check 3: Document has title
    has_title = bool(extraction.title and extraction.title.strip())
    print(f"\n✓ Document has title: {'Yes' if has_title else 'No'}")
    if has_title:
        print(f"  Title: {extraction.title}")

    # Check 4: Reading order complexity
    multi_column_pages = 0
    for page in extraction.pages:
        if len(page.words) > 50:
            x_coords = [w.x0 for w in page.words]
            if x_coords:
                x_range = max(x_coords) - min(x_coords)
                if x_range > page.width * 0.7:
                    multi_column_pages += 1

    print(f"\n✓ Pages with complex layout: {multi_column_pages}")


def example_5_batch_processing():
    """Example 5: Batch process multiple PDFs."""
    print("\n" + "=" * 80)
    print("Example 5: Batch Processing")
    print("=" * 80)

    pdf_dir = Path("pdfs")  # Directory with PDFs

    if not pdf_dir.exists():
        print(f"Directory not found: {pdf_dir}")
        print("Create a 'pdfs' directory and add PDF files to it")
        return

    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return

    print(f"Processing {len(pdf_files)} PDFs...")

    results = []

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")

        try:
            # Extract and analyze
            extractor = PDFExtractor(pdf_path=str(pdf_file), extract_images=True)
            extraction = extractor.extract()

            from pdf_workflow import PDFAccessibilityAnalyzer
            analyzer = PDFAccessibilityAnalyzer(extraction)
            report = analyzer.analyze()

            results.append({
                'file': pdf_file.name,
                'pages': extraction.num_pages,
                'issues': len(report.issues),
                'critical': report.critical_count,
                'high': report.high_count
            })

            print(f"  Issues: {len(report.issues)} "
                  f"(Critical: {report.critical_count}, High: {report.high_count})")

        except Exception as e:
            print(f"  Error: {e}")
            results.append({
                'file': pdf_file.name,
                'error': str(e)
            })

    # Summary
    print("\n" + "=" * 80)
    print("Batch Processing Summary")
    print("=" * 80)

    for result in results:
        if 'error' in result:
            print(f"✗ {result['file']}: Error - {result['error']}")
        else:
            print(f"✓ {result['file']}: {result['issues']} issues "
                  f"({result['critical']} critical, {result['high']} high)")


def main():
    """Run examples."""
    print("PDF Accessibility Workflow - Integration Examples")
    print("=" * 80)
    print()

    examples = [
        ("Basic Workflow", example_1_basic_workflow),
        ("Analysis Only", example_2_analysis_only),
        ("Step-by-Step", example_3_step_by_step),
        ("Custom Analysis", example_4_custom_analysis),
        ("Batch Processing", example_5_batch_processing),
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
                print(f"\nError in {name}: {e}")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        name, func = examples[int(choice) - 1]
        try:
            func()
        except Exception as e:
            print(f"\nError: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
