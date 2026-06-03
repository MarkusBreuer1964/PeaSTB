"""pea03_analyzer.py - Analyzer for Python Environment - Analyzer (PeaSTB)
Name, Organisation:         Markus Breuer, STMB
Erstellt, Letzte Änderung:  01.06.2026
"""

import platform
import sys
import shutil
import subprocess


def analyze_environment():
    """Collect environment data and return it as section dictionaries."""
    pip_paths_info = determine_pip_paths()
    sections = [
        create_operating_system_section(),
        create_used_python_section(),
        create_pip_paths_section(),
        create_versions_section(pip_paths_info),
    ]
    return sections


def get_cmd_output(cmd):
    """Run a command and return its combined output."""
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        output = result.stdout.strip()
        return output
    except Exception as e:
        error_message = f"Error while running {' '.join(cmd)}: {e}"
        return error_message


def find_executable(name):
    """Return the path of an executable or a not-found marker."""
    path = shutil.which(name)
    if path:
        executable_path = path
    else:
        executable_path = "Not found"
    return executable_path


def create_operating_system_section():
    """Return the operating system section."""
    content = determine_operating_system()
    section = {
        "title": "Operating System Information",
        "content": content,
    }
    return section


def create_used_python_section():
    """Return the used Python section."""
    content = determine_used_python()
    section = {
        "title": "Used Python Information",
        "content": content,
    }
    return section


def create_pip_paths_section():
    """Return the pip paths section."""
    content = determine_pip_paths()
    section = {
        "title": "Pip Paths Information",
        "content": content,
    }
    return section


def create_versions_section(pip_paths_info):
    """Return the versions section."""
    content = determine_versions(pip_paths_info)
    section = {
        "title": "Versions",
        "content": content,
    }
    return section


def determine_used_python():
    """Return the currently used Python information."""
    used_python_info = {
        "Path": sys.executable,
        "Version": platform.python_version(),
    }
    return used_python_info


def determine_pip_paths():
    """Return the available pip executable paths."""
    pip_paths_info = {
        "pip Path": find_executable("pip"),
        "pip3 Path": find_executable("pip3"),
    }
    return pip_paths_info


def determine_versions(pip_paths_info):
    """Return Python and pip version information."""
    pip_path = pip_paths_info["pip Path"]
    pip3_path = pip_paths_info["pip3 Path"]

    if pip_path != "Not found":
        pip_version = get_cmd_output([pip_path, "--version"])
    else:
        pip_version = "pip not found"

    if pip3_path != "Not found":
        pip3_version = get_cmd_output([pip3_path, "--version"])
    else:
        pip3_version = "pip3 not found"

    versions_info = {
        "python --version": get_cmd_output([sys.executable, "--version"]),
        "pip --version": pip_version,
        "pip3 --version": pip3_version,
    }
    return versions_info


def determine_operating_system():
    """Return basic operating system information."""
    operating_system_info = {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
    }
    return operating_system_info
