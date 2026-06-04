# PeaSTB - Python Environment Analyzer

PeaSTB analyzes your current Python environment and prints a structured report.

## Installation

Install from PyPI:

```bash
python -m pip install peastb
```

## Usage

Show help:

```bash
peastb --help
```

```text
usage: peastb [-h] [--version] [--analyze] [--outputfile OUTPUTFILE] [--outputfileonly]
              [--packagefile PACKAGEFILE]

PeaSTB - Python Environment Analyzer

options:
  -h, --help            show this help message and exit
  --version             Shows the current version fo the Python Environment Analyzer.
  --analyze             Analyzes the Python Environment.
  --outputfile OUTPUTFILE
                        Writes the analysis output to the given file path.
  --outputfileonly      Writes output only to the output file. Requires --outputfile.
  --packagefile PACKAGEFILE
                        Path to a text file with package names (one package per line) to check
                        imports for.
```

Run an environment analysis with package checks:

```bash
peastb --analyze --packagefile sample_packages.txt
```

Run as a module:

```bash
python -m peastb.pea01_main --analyze --packagefile sample_packages.txt
```

## Package File Example

Example file: [sample_packages.txt](sample_packages.txt)

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
