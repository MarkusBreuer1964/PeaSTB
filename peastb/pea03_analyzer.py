"""pea03_analyzer.py - Analyzer for Python Environment - Analyzer (PeaSTB)
Name, Organisation:         Markus Breuer, STMB
Created, Last updated:      01.06.2026, 04.06.2026
"""

import platform
import site
import sys
import shutil
import subprocess
import logging

from pea05_utilities import append_section

logger = logging.getLogger(__name__)


def analyze_environment():
    """Collect environment data and return it as section dictionaries."""
    pip_paths_info = determine_pip_paths()
    sections = []
    append_section(sections, create_operating_system_section, logger)
    append_section(sections, create_used_python_section, logger)
    append_section(sections, create_environment_paths_section, logger)
    append_section(sections, create_pip_paths_section, logger)
    append_section(sections, lambda: create_versions_section(pip_paths_info), logger)
    append_section(sections, create_module_search_paths_section, logger)
    append_section(sections, create_site_packages_section, logger)
    append_section(sections, create_user_site_packages_section, logger)
    append_section(sections, create_virtual_environment_section, logger)
    return sections


def get_cmd_output(cmd):
    """Run a command and return its combined output."""
    logger.debug("OS command call: %s", " ".join(cmd))
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
        output = result.stdout.strip()
        return output
    except Exception:
        logger.exception("Failed OS command call: %s", " ".join(cmd))
        error_message = f"Error while running {' '.join(cmd)}"
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
        "title": "Operating System Information (platform)",
        "content": content,
    }
    return section


def create_used_python_section():
    """Return the used Python section."""
    content = determine_used_python()
    section = {
        "title": "Used Python Information (sys.executable, platform.python_version)",
        "content": content,
    }
    return section


def create_pip_paths_section():
    """Return the pip paths section."""
    content = determine_pip_paths()
    section = {
        "title": "Pip Executable Paths (shutil.which)",
        "content": content,
    }
    return section


def create_environment_paths_section():
    """Return the environment paths section."""
    content = determine_environment_paths()
    section = {
        "title": "Environment Paths (which/where)",
        "content": content,
    }
    return section


def create_versions_section(pip_paths_info):
    """Return the versions section."""
    content = determine_versions(pip_paths_info)
    section = {
        "title": "Version Information (--version)",
        "content": content,
    }
    return section


def create_module_search_paths_section():
    """Return the section with Python module search paths."""
    content = determine_module_search_paths()
    section = {
        "title": "Module Search Paths (sys.path)",
        "content": content,
    }
    return section


def create_site_packages_section():
    """Return the section with site-packages paths."""
    content = determine_site_packages_paths()
    section = {
        "title": "Site Packages Paths (site.getsitepackages)",
        "content": content,
    }
    return section


def create_user_site_packages_section():
    """Return the section with user site-packages paths."""
    content = determine_user_site_packages_paths()
    section = {
        "title": "User Site Packages Paths (site.getusersitepackages)",
        "content": content,
    }
    return section


def create_virtual_environment_section():
    """Return the section with virtual environment status."""
    content = determine_virtual_environment()
    section = {
        "title": "Virtual Environment Status (sys.prefix vs sys.base_prefix)",
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


def determine_environment_paths():
    """Return OS-level reachability and paths for python and pip."""
    python_paths = determine_command_paths("python")
    pip_paths = determine_command_paths("pip")

    if python_paths != "Not found":
        python_reachable = "yes"
    else:
        python_reachable = "no"

    if pip_paths != "Not found":
        pip_reachable = "yes"
    else:
        pip_reachable = "no"

    environment_paths = {
        "Python Reachable": python_reachable,
        "Python Paths": python_paths,
        "Pip Reachable": pip_reachable,
        "Pip Paths": pip_paths,
    }
    return environment_paths


def determine_command_paths(command_name):
    """Return all command paths resolved by which/where as one string."""
    system_name = platform.system()

    if system_name == "Windows":
        locator_command = ["where", command_name]
    else:
        locator_command = ["which", "-a", command_name]

    locator_output = get_cmd_output(locator_command)
    output_lines = locator_output.splitlines()

    cleaned_paths = []
    for line in output_lines:
        stripped_line = line.strip()
        if stripped_line and stripped_line not in cleaned_paths:
            cleaned_paths.append(stripped_line)

    if cleaned_paths:
        resolved_paths = " | ".join(cleaned_paths)
    else:
        resolved_paths = "Not found"

    return resolved_paths


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


def determine_module_search_paths():
    """Return Python's module search paths from sys.path."""
    module_search_paths = {f"Path {index + 1}": path for index, path in enumerate(sys.path)}
    return module_search_paths


def determine_site_packages_paths():
    """Return paths reported by site.getsitepackages()."""
    try:
        site_packages = site.getsitepackages()
    except Exception:
        site_packages = []

    site_packages_paths = {f"Site Package Path {index + 1}": path for index, path in enumerate(site_packages)}

    if not site_packages_paths:
        site_packages_paths = {
            "Site Package Path": "Not available",
        }

    return site_packages_paths


def determine_user_site_packages_paths():
    """Return path reported by site.getusersitepackages()."""
    try:
        user_site_packages = site.getusersitepackages()
    except Exception:
        user_site_packages = None

    if user_site_packages:
        user_site_packages_paths = {
            "User Site Package Path": user_site_packages,
        }
    else:
        user_site_packages_paths = {
            "User Site Package Path": "Not available",
        }

    return user_site_packages_paths


def determine_virtual_environment():
    """Return the virtual environment status and location if active."""
    virtual_environment_active = sys.prefix != sys.base_prefix

    if virtual_environment_active:
        virtual_environment_state = "active"
        virtual_environment_path = sys.prefix
    else:
        virtual_environment_state = "not active"
        virtual_environment_path = "Not active"

    virtual_environment_info = {
        "Virtual Environment Status": virtual_environment_state,
        "Virtual Environment Path": virtual_environment_path,
        "Base Prefix": sys.base_prefix,
    }
    return virtual_environment_info


def determine_operating_system():
    """Return basic operating system information."""
    operating_system_info = {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
    }
    return operating_system_info
