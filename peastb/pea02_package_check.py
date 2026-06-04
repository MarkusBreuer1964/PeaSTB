"""pea02_analyzer.py - Analyzer for Python Environment (PeaSTB) - Package Checker
Name, Organisation:         Markus Breuer, STMB
Erstellt, Letzte Änderung:  31.06.2026, 04.06.2026
"""
import importlib
import json
import subprocess
import sys
from pathlib import Path


def run_package_check(packagefile=None):
    """Run the package check and return all package-check sections."""
    installed_packages = list_installed_packages()

    if packagefile:
        package_list = load_package_list_from_file(packagefile)
        import_results = check_package_imports(package_list)
        sections = [
            create_package_imports_section(import_results),
            create_package_summary_section(import_results),
            create_installed_packages_section(installed_packages),
        ]
        return sections

    sections = [
        create_installed_packages_section(installed_packages),
    ]
    return sections


def load_package_list_from_file(packagefile):
    """Load package names from a text file (one package per line)."""
    packagefile_path = Path(packagefile)
    with packagefile_path.open("r", encoding="utf-8") as file:
        packages = [
            line.strip()
            for line in file
            if line.strip() and not line.lstrip().startswith("#")
        ]
    if not packages:
        raise ValueError("The provided package file does not contain any packages.")
    return packages


def check_package_imports(package_list):
    """Attempt to import each package and return a dictionary with results."""
    import_results = {}
    for package in package_list:
        try:
            importlib.import_module(package)
            import_results[package] = "successful"
        except Exception:
            import_results[package] = "not successful"
    return import_results


def list_installed_packages():
    """Return installed packages as name -> 'version -> location'."""
    command = [sys.executable, "-m", "pip", "list", "--format=json", "--verbose"]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if result.returncode != 0:
        error_content = {"pip": f"not available | {result.stdout.strip()}"}
        return error_content

    raw_output = result.stdout
    packages_data = json.loads(raw_output)

    installed_packages = {}
    for package in packages_data:
        package_name = package.get("name", "unknown")
        package_version = package.get("version", "unknown version")
        package_location = package.get("location", "unknown location")
        package_value = f"{package_version} -> {package_location}"
        installed_packages[package_name] = package_value

    return installed_packages


def create_package_imports_section(import_results):
    """Return the section with import results for each package."""
    content = import_results
    section = {
        "title": "Package Import Check",
        "content": content,
    }
    return section


def create_package_summary_section(import_results):
    """Return the summary section for the import results."""
    successful_imports = sum(
        1 for result in import_results.values() if result == "successful"
    )
    failed_imports = sum(
        1 for result in import_results.values() if result == "not successful"
    )
    content = {
        "Successful Imports": successful_imports,
        "Failed Imports": failed_imports,
    }
    section = {
        "title": "Package Import Summary",
        "content": content,
    }
    return section


def create_installed_packages_section(installed_packages):
    """Return the section with installed packages from pip list -v."""
    content = installed_packages
    section = {
        "title": "Installed Packages",
        "content": content,
    }
    return section
