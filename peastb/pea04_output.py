"""pea04_output.py - Output Service for Python Environment Analyzer (PeaSTB)."""

from datetime import datetime
import getpass
import socket
import logging

try:
    from . import version
except ImportError:
    import version


logger = logging.getLogger(__name__)


def determine_title_information(title):
    """Return title metadata used in reports."""
    title_information = {
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "computer_name": socket.gethostname(),
        "user_name": getpass.getuser(),
        "peastb_version": version.PEASTB_VERSION,
        "peastb_version_date": version.PEASTB_VERSION_DATE,
    }
    return title_information


def create_introduction_section(title_information):
    """Return the introduction section based on the report metadata."""
    return {
        "title": title_information["title"],
        "content": {
            "Date": title_information["date"],
            "Computer name": title_information["computer_name"],
            "User name": title_information["user_name"],
            "PeaSTB version": title_information.get(
                "peastb_version", version.PEASTB_VERSION
            ),
            "PeaSTB Version Date": title_information.get(
                "peastb_version_date", version.PEASTB_VERSION_DATE
            ),
        },
    }


def format_section(section):
    """Return formatted report lines for a section dictionary."""
    title = section["title"]
    content = section["content"]
    lines = [title, "-" * len(title)]
    max_key_length = max((len(str(key)) for key in content), default=0)
    for key, value in content.items():
        lines.append(f"{key:<{max_key_length}}: {value}")
    lines.append("")
    return lines


def build_report(title_information, sections):
    """Build a full report string from title metadata and section dictionaries."""
    lines = []
    all_sections = [create_introduction_section(title_information), *sections]
    for section in all_sections:
        lines.extend(format_section(section))
    report = "\n".join(lines)
    return report


def emit_report(report, outputfile=None, outputfileonly=False):
    """Write report to terminal and/or file based on output arguments."""
    if not outputfileonly:
        print(report, end="")
    if outputfile:
        with open(outputfile, "w", encoding="utf-8") as file:
            file.write(report)
        logger.info("Analysis report written to output file: %s", outputfile)
