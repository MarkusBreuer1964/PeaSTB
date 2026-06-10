# PeaSTB - Python Environment Analyzer

PeaSTB inspects your current Python environment and prints a structured report.

## What It Reports

PeaSTB can report the following information:

- Report metadata: date, computer name, and user name
- Operating System Information (platform): system, release, version, and architecture
- Used Python Information (sys.executable, platform.python_version): executable path and Python version
- Environment Paths (which/where): reachable Python and pip commands with resolved paths
- Pip Executable Paths (shutil.which): detected pip and pip3 executables
- Version Information (--version): output of python --version, pip --version, and pip3 --version
- Installed Packages (pip list --verbose): package name mapped to version and installation path
- Module Search Paths (sys.path): Python module search path entries from sys.path
- Site Packages Paths (site.getsitepackages): paths returned by site.getsitepackages()
- User Site Packages Paths (site.getusersitepackages): user-level site-packages path
- Virtual Environment Status (sys.prefix vs sys.base_prefix): whether a virtual environment is active and where it is located

If you provide --packagefile, PeaSTB also adds:

- Package Import Check (importlib.import_module): per-package import result
- Package Import Summary (count): counts of successful and failed imports

## Installation

Install from PyPI with pip:

```bash
pip install peastb
```

or

```bash
python -m pip install peastb
```

## Usage

Show the command-line help:

```bash
peastb --help
```

Help text:

```text
usage: peastb [-h] [--version] [--analyze] [--outputfile OUTPUTFILE] [--outputfileonly]
              [--packagefile PACKAGEFILE] [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

PeaSTB - Python Environment Analyzer

options:
  -h, --help            show this help message and exit
  --version             Shows the current version of the Python Environment Analyzer.
  --analyze             Analyzes the Python Environment.
  --outputfile OUTPUTFILE
                        Writes the analysis output to the given file path.
  --outputfileonly      Writes output only to the output file. Requires --outputfile.
  --packagefile PACKAGEFILE
                        Path to a text file with package names (one package per line) to check
                        imports for.
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Sets the log level for peastb.log (default: INFO).
```

Logging:

- Log file: peastb.log
- Existing content is preserved (append mode)
- Default log level: INFO

Example with debug logging:

```bash
peastb --analyze --loglevel DEBUG
```

Run a full analysis with package checks:

```bash
peastb --analyze --packagefile sample_packages.txt
```

You can also run the module directly:

```bash
python -m peastb.pea01_main --analyze --packagefile sample_packages.txt
```

## Package File Example

```text
# sample package list
sys
colorama
non_existing_demo_package
```

A package file tailored to the BK GuT environment is included in the GitHub repository.

## Version

Current version: 0.1.0a2

## Repository

Source code and project history are available on GitHub:

- https://github.com/MarkusBreuer1964/PeaSTB

## License

[MIT](LICENSE.txt) © Markus Breuer.
