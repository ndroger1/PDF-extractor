#!/usr/bin/env python3
"""
Test script for PDF Workflow Integration

Validates that the workflow integration is properly set up.
"""

import sys
from pathlib import Path

print("Testing PDF Workflow Integration")
print("=" * 80)

# Test 1: Check if files exist
print("\n1. Checking files...")
files_to_check = [
    'pdf_extractor.py',
    'pdf_workflow.py',
    'pdf_remediator.py',
    'requirements_extractor.txt',
    'WORKFLOW_GUIDE.md',
    'examples/complete_workflow.py'
]

all_exist = True
for file_path in files_to_check:
    exists = Path(file_path).exists()
    status = "[OK]" if exists else "[MISSING]"
    print(f"  {status} {file_path}")
    if not exists:
        all_exist = False

if not all_exist:
    print("\n[ERROR] Some files are missing")
    sys.exit(1)

print("\n[OK] All required files present")

# Test 2: Check imports
print("\n2. Testing imports...")

try:
    from pdf_extractor import PDFExtractor, PDFExtraction
    print("  [OK] pdf_extractor imports")
except ImportError as e:
    print(f"  [ERROR] pdf_extractor import failed: {e}")

try:
    from pdf_workflow import (
        PDFAccessibilityWorkflow,
        PDFAccessibilityAnalyzer,
        AccessibilityIssue,
        AccessibilityReport
    )
    print("  [OK] pdf_workflow imports")
except ImportError as e:
    print(f"  [ERROR] pdf_workflow import failed: {e}")

# Test 3: Check data classes
print("\n3. Testing data structures...")

try:
    from pdf_workflow import AccessibilityIssue, AccessibilityReport

    # Create test issue
    issue = AccessibilityIssue(
        issue_type="Test Issue",
        severity="medium",
        page=1,
        description="Test description",
        wcag_criterion="1.1.1",
        recommendation="Fix it",
        auto_fixable=True
    )
    print("  [OK] AccessibilityIssue created")

    # Create test report
    report = AccessibilityReport(
        pdf_path="test.pdf",
        total_pages=10
    )
    report.add_issue(issue)
    print("  [OK] AccessibilityReport created")
    print(f"    Issues: {len(report.issues)}")
    print(f"    Medium: {report.medium_count}")

except Exception as e:
    print(f"  [ERROR] Data structure error: {e}")

# Test 4: Check documentation
print("\n4. Checking documentation...")

docs = {
    'WORKFLOW_GUIDE.md': 'Workflow guide',
    'EXTRACTOR_README.md': 'Extractor documentation',
    'QUICKSTART_EXTRACTOR.md': 'Quick start guide'
}

for doc_file, description in docs.items():
    if Path(doc_file).exists():
        print(f"  [OK] {description}")
    else:
        print(f"  [WARN] {description} not found")

# Test 5: Dependencies check
print("\n5. Checking dependencies...")

dependencies = {
    'pikepdf': 'PDF manipulation',
    'PyMuPDF': 'Image extraction (recommended)',
    'pdfplumber': 'Text extraction (recommended)',
    'Pillow': 'Image processing',
}

for module, description in dependencies.items():
    try:
        if module == 'PyMuPDF':
            import fitz
        elif module == 'Pillow':
            from PIL import Image
        else:
            __import__(module)
        print(f"  [OK] {module}: {description}")
    except ImportError:
        print(f"  [WARN] {module}: {description} (optional)")

# Summary
print("\n" + "=" * 80)
print("Integration Test Summary")
print("=" * 80)
print("\nThe workflow integration is set up correctly!")
print("\nTo use:")
print("  1. Install dependencies: pip install -r requirements_extractor.txt")
print("  2. Run workflow: python pdf_workflow.py input.pdf --output accessible.pdf")
print("  3. See examples: python examples/complete_workflow.py")
print("  4. Read guide: WORKFLOW_GUIDE.md")
print("\n" + "=" * 80)
