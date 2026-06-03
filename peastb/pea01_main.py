"""pea01_main.py - CLI-Interface for Python Environment Analyzer (PeaSTB)
Name, Organisaion:          Markus Breuer, STMB
Erstellt, Letzte Änderung:  30.05.2026, 31.05.2026
"""

import sys
import argparse
import pea03_analyzer as analyzer
import pea02_package_check as package_check
import pea04_output as output_service
import version


def analyze(include_environment=False, packagefile=None):
    """Run the requested analysis steps and return report sections."""
    report_sections = []

    if include_environment:
        report_sections.extend(analyzer.analyze_environment())

    if packagefile:
        report_sections.extend(package_check.run_package_check(packagefile=packagefile))

    return report_sections


def main():
    """Main function to handle command-line arguments and execute actions."""
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="PeaSTB - Python Environment Analyzer")
    parser.add_argument(
        "--version",
        action="store_true",
        help="Shows the current version fo the Python Environment Analyzer.",
    )
    parser.add_argument(
        "--analyze", action="store_true", help="Analyzes the Python Environment."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        help="Writes the analysis output to the given file path.",
    )
    parser.add_argument(
        "--outputfileonly",
        action="store_true",
        help="Writes output only to the output file. Requires --outputfile.",
    )
    parser.add_argument(
        "--packagefile",
        type=str,
        help="Path to a text file with package names (one package per line) to check imports for.",
    )
    args = parser.parse_args()

    if args.outputfileonly and not args.outputfile:
        parser.error("--outputfileonly requires --outputfile")

    # Handle command-line arguments
    action_executed = False
    report_sections = []

    if args.version:
        print(f"Version: {version.PEASTB_VERSION}")
        print(f"Version Date: {version.PEASTB_VERSION_DATE}")
        action_executed = True

    if args.analyze:
        action_executed = True
        try:
            report_sections = analyze(
                include_environment=args.analyze,
                packagefile=args.packagefile,
            )
        except FileNotFoundError:
            parser.error(f"Package file not found: {args.packagefile}")
        except ValueError as exc:
            parser.error(str(exc))
    elif args.packagefile:
        action_executed = True
        try:
            report_sections = analyze(packagefile=args.packagefile)
        except FileNotFoundError:
            parser.error(f"Package file not found: {args.packagefile}")
        except ValueError as exc:
            parser.error(str(exc))

    if report_sections:
        title_information = output_service.determine_title_information(
            "Python Environment Analyzer (PeaSTB)"
        )
        report = output_service.build_report(title_information, report_sections)
        output_service.emit_report(
            report,
            outputfile=args.outputfile,
            outputfileonly=args.outputfileonly,
        )

    if not action_executed:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
