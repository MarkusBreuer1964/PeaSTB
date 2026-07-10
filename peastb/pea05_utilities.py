"""pea05_utilities.py - Shared helper functions for Python Environment Analyzer (PeaSTB)
Name, Organisation:         Markus Breuer, STMB
Created, Last updated:      12.06.2026, 12.06.2026
"""


def append_section(sections, section_factory, logger):
    """Create a section, append it, and continue on errors."""
    try:
        section = section_factory()
        sections.append(section)
        logger.info("Section created: %s", section.get("title", "Unknown section"))
    except Exception:
        logger.exception("Section could not be created: %s", section_factory.__name__)
