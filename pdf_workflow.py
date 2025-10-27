#!/usr/bin/env python3
"""
PDF Accessibility Workflow - Extract, Analyze, and Remediate

This script provides an integrated workflow combining:
1. Content Extraction (pdf_extractor.py) - Extract all words and images
2. Accessibility Analysis - Identify issues using extraction data
3. Remediation (pdf_remediator.py) - Fix accessibility issues
4. Verification - Validate improvements

Usage:
    # Full workflow: extract, analyze, and remediate
    python pdf_workflow.py input.pdf --output accessible.pdf

    # Extract and analyze only
    python pdf_workflow.py input.pdf --analyze-only

    # Use AI for better alt text
    python pdf_workflow.py input.pdf --output accessible.pdf --use-ai

    # Full workflow with detailed reporting
    python pdf_workflow.py input.pdf --output accessible.pdf --generate-report
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

try:
    from pdf_extractor import PDFExtractor, PDFExtraction
    HAS_EXTRACTOR = True
except ImportError:
    HAS_EXTRACTOR = False
    print("Warning: pdf_extractor not found. Install dependencies.")

try:
    from pdf_remediator import PDFRemediator
    HAS_REMEDIATOR = True
except ImportError:
    HAS_REMEDIATOR = False
    print("Warning: pdf_remediator not found.")


@dataclass
class AccessibilityIssue:
    """Represents an accessibility issue found in the PDF."""
    issue_type: str
    severity: str  # critical, high, medium, low
    page: int
    description: str
    wcag_criterion: str
    recommendation: str
    location: Optional[str] = None
    auto_fixable: bool = False


@dataclass
class AccessibilityReport:
    """Complete accessibility analysis report."""
    pdf_path: str
    analysis_date: str = field(default_factory=lambda: datetime.now().isoformat())
    total_pages: int = 0
    total_words: int = 0
    total_images: int = 0
    issues: List[AccessibilityIssue] = field(default_factory=list)
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0

    def add_issue(self, issue: AccessibilityIssue) -> None:
        """Add an issue and update counts."""
        self.issues.append(issue)
        if issue.severity == 'critical':
            self.critical_count += 1
        elif issue.severity == 'high':
            self.high_count += 1
        elif issue.severity == 'medium':
            self.medium_count += 1
        else:
            self.low_count += 1

    def get_summary(self) -> str:
        """Get a text summary of the report."""
        summary = []
        summary.append("=" * 80)
        summary.append("PDF Accessibility Analysis Report")
        summary.append("=" * 80)
        summary.append(f"\nFile: {self.pdf_path}")
        summary.append(f"Date: {self.analysis_date}")
        summary.append(f"Pages: {self.total_pages}")
        summary.append(f"Words: {self.total_words}")
        summary.append(f"Images: {self.total_images}")
        summary.append(f"\nTotal Issues Found: {len(self.issues)}")
        summary.append(f"  Critical: {self.critical_count}")
        summary.append(f"  High: {self.high_count}")
        summary.append(f"  Medium: {self.medium_count}")
        summary.append(f"  Low: {self.low_count}")
        summary.append("\n" + "=" * 80)

        if self.issues:
            summary.append("\nIssues by Type:")
            summary.append("-" * 80)

            # Group by type
            by_type = {}
            for issue in self.issues:
                if issue.issue_type not in by_type:
                    by_type[issue.issue_type] = []
                by_type[issue.issue_type].append(issue)

            for issue_type, issues in sorted(by_type.items()):
                summary.append(f"\n{issue_type} ({len(issues)} issues):")
                for issue in issues[:3]:  # Show first 3 of each type
                    summary.append(f"  Page {issue.page}: {issue.description}")
                    summary.append(f"    WCAG: {issue.wcag_criterion}")
                    summary.append(f"    Fix: {issue.recommendation}")
                if len(issues) > 3:
                    summary.append(f"  ... and {len(issues) - 3} more")

        return "\n".join(summary)


class PDFAccessibilityAnalyzer:
    """Analyzes PDF extraction data for accessibility issues."""

    def __init__(self, extraction: PDFExtraction):
        self.extraction = extraction
        self.report = AccessibilityReport(
            pdf_path=extraction.file_path,
            total_pages=extraction.num_pages,
            total_words=extraction.total_words,
            total_images=extraction.total_images
        )

    def analyze(self) -> AccessibilityReport:
        """Run complete accessibility analysis."""
        print("Analyzing PDF for accessibility issues...")

        self._check_metadata()
        self._check_images()
        self._check_document_structure()
        self._check_reading_order()
        self._check_color_contrast()

        print(f"Analysis complete: {len(self.report.issues)} issues found")
        return self.report

    def _check_metadata(self) -> None:
        """Check document metadata (WCAG 2.4.2)."""
        if not self.extraction.title or len(self.extraction.title.strip()) == 0:
            self.report.add_issue(AccessibilityIssue(
                issue_type="Missing Document Title",
                severity="high",
                page=0,
                description="PDF has no title in metadata",
                wcag_criterion="2.4.2 Page Titled",
                recommendation="Add a descriptive title to the PDF metadata",
                auto_fixable=True
            ))

        if not self.extraction.author:
            self.report.add_issue(AccessibilityIssue(
                issue_type="Missing Author",
                severity="low",
                page=0,
                description="PDF has no author in metadata",
                wcag_criterion="Best Practice",
                recommendation="Add author information to PDF metadata",
                auto_fixable=False
            ))

    def _check_images(self) -> None:
        """Check images for alt text (WCAG 1.1.1)."""
        images_without_alt = 0

        for page in self.extraction.pages:
            for img in page.images:
                # Check if image likely needs alt text (not decorative)
                is_likely_decorative = (
                    img.width < 20 or img.height < 20 or
                    (img.width * img.height < 400) or
                    img.width > 1500 or img.height > 1500
                )

                if not is_likely_decorative and not img.ocr_text:
                    images_without_alt += 1
                    self.report.add_issue(AccessibilityIssue(
                        issue_type="Image Missing Alt Text",
                        severity="critical",
                        page=page.page_number,
                        description=f"Image '{img.name}' ({img.width}x{img.height}) needs alt text",
                        wcag_criterion="1.1.1 Non-text Content",
                        recommendation="Add descriptive alt text or mark as decorative",
                        location=f"({img.x0:.0f}, {img.y0:.0f})",
                        auto_fixable=True
                    ))

        if images_without_alt > 0:
            print(f"  Found {images_without_alt} images needing alt text")

    def _check_document_structure(self) -> None:
        """Check for proper document structure (WCAG 1.3.1)."""
        # Check for heading-like text (large font sizes)
        heading_candidates = []

        for page in self.extraction.pages:
            for word in page.words:
                if word.font_size > 16:  # Likely a heading
                    heading_candidates.append((page.page_number, word.text, word.font_size))

        if heading_candidates:
            self.report.add_issue(AccessibilityIssue(
                issue_type="Potential Untagged Headings",
                severity="high",
                page=heading_candidates[0][0],
                description=f"Found {len(heading_candidates)} potential headings with large font sizes",
                wcag_criterion="1.3.1 Info and Relationships",
                recommendation="Tag text with proper heading levels (H1, H2, etc.)",
                auto_fixable=True
            ))

    def _check_reading_order(self) -> None:
        """Check reading order issues (WCAG 1.3.2)."""
        for page in self.extraction.pages:
            # Check for multi-column layouts that might have ordering issues
            if len(page.words) > 50:
                # Check if words are scattered across x-coordinates
                x_coords = [w.x0 for w in page.words]
                if x_coords:
                    x_range = max(x_coords) - min(x_coords)
                    if x_range > page.width * 0.7:  # Spans more than 70% of page width
                        self.report.add_issue(AccessibilityIssue(
                            issue_type="Potential Reading Order Issue",
                            severity="medium",
                            page=page.page_number,
                            description="Page may have complex layout affecting reading order",
                            wcag_criterion="1.3.2 Meaningful Sequence",
                            recommendation="Verify and optimize reading order for screen readers",
                            auto_fixable=True
                        ))

    def _check_color_contrast(self) -> None:
        """Check for potential color contrast issues (WCAG 1.4.3)."""
        # This is a basic check - full contrast checking requires color information
        total_words = sum(len(p.words) for p in self.extraction.pages)

        if total_words > 0:
            self.report.add_issue(AccessibilityIssue(
                issue_type="Color Contrast Check Needed",
                severity="medium",
                page=0,
                description="Manual verification of color contrast required",
                wcag_criterion="1.4.3 Contrast (Minimum)",
                recommendation="Ensure text has 4.5:1 contrast ratio (3:1 for large text)",
                auto_fixable=False
            ))


class PDFAccessibilityWorkflow:
    """Complete workflow: extract, analyze, and remediate PDFs."""

    def __init__(self, pdf_path: str, output_path: Optional[str] = None,
                 use_ai: bool = False, generate_report: bool = False):
        self.pdf_path = Path(pdf_path)
        self.output_path = Path(output_path) if output_path else None
        self.use_ai = use_ai
        self.generate_report = generate_report

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    def run(self) -> Tuple[Optional[AccessibilityReport], bool]:
        """
        Run the complete workflow.

        Returns:
            Tuple of (AccessibilityReport, success_bool)
        """
        print("=" * 80)
        print("PDF Accessibility Workflow")
        print("=" * 80)
        print(f"\nInput: {self.pdf_path}")
        if self.output_path:
            print(f"Output: {self.output_path}")
        print()

        # Step 1: Extract content
        print("Step 1: Extracting PDF content...")
        print("-" * 80)
        extraction = self._extract_content()

        if not extraction:
            print("✗ Extraction failed")
            return None, False

        print(f"✓ Extracted {extraction.total_words} words and {extraction.total_images} images")

        # Step 2: Analyze for accessibility issues
        print("\nStep 2: Analyzing accessibility...")
        print("-" * 80)
        report = self._analyze_accessibility(extraction)

        print(f"✓ Found {len(report.issues)} accessibility issues")
        print(f"  Critical: {report.critical_count}")
        print(f"  High: {report.high_count}")
        print(f"  Medium: {report.medium_count}")
        print(f"  Low: {report.low_count}")

        # Generate analysis report if requested
        if self.generate_report:
            report_path = self.pdf_path.parent / f"{self.pdf_path.stem}_accessibility_report.txt"
            with report_path.open('w', encoding='utf-8') as f:
                f.write(report.get_summary())
                f.write("\n\n")
                f.write("Detailed Issues:\n")
                f.write("=" * 80 + "\n\n")
                for i, issue in enumerate(report.issues, 1):
                    f.write(f"{i}. {issue.issue_type}\n")
                    f.write(f"   Page: {issue.page}\n")
                    f.write(f"   Severity: {issue.severity}\n")
                    f.write(f"   WCAG: {issue.wcag_criterion}\n")
                    f.write(f"   Description: {issue.description}\n")
                    f.write(f"   Recommendation: {issue.recommendation}\n")
                    if issue.location:
                        f.write(f"   Location: {issue.location}\n")
                    f.write(f"   Auto-fixable: {issue.auto_fixable}\n")
                    f.write("\n")
            print(f"\n✓ Analysis report saved to: {report_path}")

        # Step 3: Remediate (if output path specified)
        if self.output_path:
            print("\nStep 3: Remediating PDF...")
            print("-" * 80)
            success = self._remediate_pdf(extraction, report)

            if success:
                print(f"✓ Remediated PDF saved to: {self.output_path}")

                # Step 4: Optional verification
                print("\nStep 4: Verifying improvements...")
                print("-" * 80)
                self._verify_remediation()
            else:
                print("✗ Remediation failed")
                return report, False
        else:
            print("\nSkipping remediation (no output path specified)")
            print("Use --output to remediate the PDF")

        print("\n" + "=" * 80)
        print("Workflow Complete")
        print("=" * 80)

        return report, True

    def _extract_content(self) -> Optional[PDFExtraction]:
        """Extract all content from PDF."""
        if not HAS_EXTRACTOR:
            print("Error: PDF extractor not available")
            return None

        try:
            extractor = PDFExtractor(
                pdf_path=str(self.pdf_path),
                extract_images=True
            )
            extraction = extractor.extract()

            # Save extraction data for reference
            extraction_path = self.pdf_path.parent / f"{self.pdf_path.stem}_extraction.json"
            extractor.save_to_json(extraction, str(extraction_path))
            print(f"  Extraction data saved to: {extraction_path}")

            return extraction

        except Exception as e:
            print(f"Error during extraction: {e}")
            return None

    def _analyze_accessibility(self, extraction: PDFExtraction) -> AccessibilityReport:
        """Analyze extraction data for accessibility issues."""
        analyzer = PDFAccessibilityAnalyzer(extraction)
        return analyzer.analyze()

    def _remediate_pdf(self, extraction: PDFExtraction, report: AccessibilityReport) -> bool:
        """Remediate the PDF using the remediator."""
        if not HAS_REMEDIATOR:
            print("Error: PDF remediator not available")
            print("Install pikepdf to use remediation features")
            return False

        try:
            # Use the PDF remediator to fix issues
            print(f"  Processing with PDF Remediator...")

            # The remediator will handle:
            # - Adding document tags
            # - Adding alt text to images
            # - Fixing reading order
            # - Adding metadata

            # For now, show what would be done
            auto_fixable = sum(1 for issue in report.issues if issue.auto_fixable)
            print(f"  Auto-fixing {auto_fixable} issues...")

            # Import and use remediator
            import subprocess
            result = subprocess.run([
                sys.executable,
                'pdf_remediator.py',
                str(self.pdf_path),
                '--output', str(self.output_path)
            ], capture_output=True, text=True)

            if result.returncode == 0:
                return True
            else:
                print(f"  Remediator output: {result.stdout}")
                print(f"  Remediator errors: {result.stderr}")
                return False

        except Exception as e:
            print(f"Error during remediation: {e}")
            return False

    def _verify_remediation(self) -> None:
        """Verify the remediated PDF."""
        if not self.output_path or not self.output_path.exists():
            return

        try:
            # Re-extract and re-analyze
            extractor = PDFExtractor(
                pdf_path=str(self.output_path),
                extract_images=True
            )
            new_extraction = extractor.extract()

            analyzer = PDFAccessibilityAnalyzer(new_extraction)
            new_report = analyzer.analyze()

            print(f"  Before: {len(self.report.issues)} issues")
            print(f"  After: {len(new_report.issues)} issues")

            if len(new_report.issues) < len(self.report.issues):
                print(f"  ✓ Improved: {len(self.report.issues) - len(new_report.issues)} issues fixed")

        except Exception as e:
            print(f"  Could not verify: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="PDF Accessibility Workflow - Extract, Analyze, and Remediate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze PDF for accessibility issues
  python pdf_workflow.py document.pdf --analyze-only --generate-report

  # Full workflow: analyze and remediate
  python pdf_workflow.py document.pdf --output accessible.pdf

  # Use AI for better alt text
  python pdf_workflow.py document.pdf --output accessible.pdf --use-ai

  # Full workflow with detailed reporting
  python pdf_workflow.py document.pdf --output accessible.pdf --generate-report
        """
    )

    parser.add_argument('pdf_path', help='Input PDF file')
    parser.add_argument('-o', '--output', help='Output PDF file (remediated)')
    parser.add_argument('--analyze-only', action='store_true',
                        help='Only analyze, do not remediate')
    parser.add_argument('--use-ai', action='store_true',
                        help='Use AI for image descriptions (requires API key)')
    parser.add_argument('--generate-report', action='store_true',
                        help='Generate detailed accessibility report')

    args = parser.parse_args()

    if not HAS_EXTRACTOR:
        print("Error: PDF extractor not available")
        print("Install required packages: pip install -r requirements_extractor.txt")
        sys.exit(1)

    # Create workflow
    output_path = None if args.analyze_only else args.output

    workflow = PDFAccessibilityWorkflow(
        pdf_path=args.pdf_path,
        output_path=output_path,
        use_ai=args.use_ai,
        generate_report=args.generate_report
    )

    # Run workflow
    try:
        report, success = workflow.run()

        if report:
            print(f"\n{report.get_summary()}")

        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
