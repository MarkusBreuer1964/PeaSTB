"""test_installation.py - System Tests testing the installation of peastb
Name, Organisation:         Markus Breuer, STMB
Created, Last updated:      10.07.2026
"""

from importlib.metadata import version
from pathlib import Path
import subprocess


def test_version():
    """ System test of peastb --version"""
    expected = version("peastb")
    result = subprocess.run(
        ["peastb", "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert expected in result.stdout

def test_analyze_creates_report_and_log():
    """ System test of peastb --analyze"""
    subprocess.run(
        [
            "peastb",
            "--analyze",
            "--outputfile",
            "test_report.txt",
            "--outputfileonly",
        ],
        capture_output=True,
        text=True,
        check=True,
        timeout=120,
    )
    assert Path("test_report.txt").exists()
    assert Path("peastb.log").exists()    