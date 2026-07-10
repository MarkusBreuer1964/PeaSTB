"""pea01_main.py - CLI-Interface for Python Environment Analyzer (PeaSTB)
Name, Organisation:         Markus Breuer, STMB
Created, Last updated:      30.05.2026, 10.06.2026
"""

import sys
import argparse
import logging
import pea03_analyzer as analyzer
import pea02_package_check as package_check
import pea04_output as output_service
import version

logger = logging.getLogger(__name__)


def configure_logging(loglevel_name):
    """Configure file logging with append mode and a fixed format."""
    resolved_level_name = str(loglevel_name).upper()
    resolved_level = getattr(logging, resolved_level_name, logging.INFO)
    logging.basicConfig(
        filename="peastb.log",
        filemode="a",
        level=resolved_level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        force=True,
    )


def analyze(include_environment=False, packagefile=None):
    """Run the requested analysis steps and return report sections."""
    report_sections = []

    if include_environment:
        report_sections.extend(analyzer.analyze_environment())

    if include_environment or packagefile:
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
    parser.add_argument("--analyze", action="store_true", help="Analyzes the Python Environment.")
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
    parser.add_argument(
        "--loglevel",
        type=str.upper,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Sets the log level for peastb.log (default: INFO).",
    )
    args = parser.parse_args()

    configure_logging(args.loglevel)
    logger.info("Program started")

    try:
        if args.outputfileonly and not args.outputfile:
            logger.error("--outputfileonly requires --outputfile")
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
            if not args.outputfile:
                print("PeaSTB: Analyzing Python environment...")
            try:
                report_sections = analyze(
                    include_environment=args.analyze,
                    packagefile=args.packagefile,
                )
            except FileNotFoundError:
                logger.exception(
                    "Program terminated early because package file was not found: %s",
                    args.packagefile,
                )
                parser.error(f"Package file not found: {args.packagefile}")
            except ValueError as exc:
                logger.exception("Program terminated early because package file could not be processed.")
                parser.error(str(exc))
        elif args.packagefile:
            action_executed = True
            try:
                report_sections = analyze(packagefile=args.packagefile)
            except FileNotFoundError:
                logger.exception(
                    "Program terminated early because package file was not found: %s",
                    args.packagefile,
                )
                parser.error(f"Package file not found: {args.packagefile}")
            except ValueError as exc:
                logger.exception("Program terminated early because package file could not be processed.")
                parser.error(str(exc))

        if report_sections:
            title_information = output_service.determine_title_information("Python Environment Analyzer (PeaSTB)")
            report = output_service.build_report(title_information, report_sections)
            output_service.emit_report(
                report,
                outputfile=args.outputfile,
                outputfileonly=args.outputfileonly,
            )

        if not action_executed:
            parser.print_help()
    finally:
        logger.info("Program finished")
        logger.info("")
        logger.info("")

    sys.exit(0)


if __name__ == "__main__":
    main()
