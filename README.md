# PeaSTB - Python Environment Analyzer

PeaSTB inspects your current Python environment and prints a structured report.

## What It Reports

PeaSTB can report the following information:

- Report metadata: date, computer name, and user name
- Operating system information: system, release, version, and architecture
- Used Python information: executable path and Python version
- Environment paths on the operating system level: reachable Python and pip commands with resolved paths
- Pip executable paths: detected pip and pip3 executables
- Version information: output of python --version, pip --version, and pip3 --version
- Installed packages: package name mapped to version and installation path
- Module search paths: Python module search path entries from sys.path
- Site packages paths: paths returned by site.getsitepackages()
- Virtual environment status: whether a virtual environment is active and where it is located

If you provide --packagefile, PeaSTB also adds:

- Package import check: per-package import result
- Package import summary: counts of successful and failed imports

## Installation

Install from PyPI with pip:

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
              [--packagefile PACKAGEFILE]

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

## Version

Current version: 0.1.0a1

## License

[MIT](LICENSE.txt) © Markus Breuer.
