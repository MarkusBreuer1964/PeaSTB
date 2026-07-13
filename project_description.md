# Project Description

This project has two objectives:

1. It provides a script that analyzes a Python environment.
2. It is a learning project for experimenting with tools, processes, and techniques used in modern Python development.

## Learning Objectives

The following tools are used in this project:

- poetry
- git
- pytest
- tox
- PyPI and TestPyPI

The following techniques have been used in this project:

- Automated component and integration tests with pytest
- System and installation tests with tox and pytest
- Publishing with PyPI and TestPyPI
- Project versioning and project building with Poetry
- Automated workflows implemented as Python scripts: quality workflow and delivery workflow
- Automatic setting of version information from a single source (`pyproject.toml`), implemented via a Python script.

## Description of the project directory structure

``` directory structure
SW04_PeaSTB                 -> root directory of the project
├── dev                     -> scripts and tools needed for development
├── dist                    -> distribution directory
├── peastb                  -> source code directory
│   └── __pycache__
├── tests                   -> component and integration tests; test files for pytest
│   └── __pycache__
└── tests_installation      -> installation tests; test files for pytest
    └── __pycache__ 
```

__SW04_PeaSTB (root directory of the project)__

The root directory contains the main project configuration and description files. It is normally the current working directory and includes the following files:

- pyproject.toml    -> Contains the main project configuration for Poetry
- poetry.toml       -> Contains central Poetry configurations
- poetry.lock       -> Exact versions of the used packages, automatically maintained by Poetry
- tox.ini           -> Description of test environments and tests executed by tox (system tests, installation tests)

__dev__

- sync_build.py      -> Synchronizes the version number and build date
- wf_quality.py      -> Quality workflow using black (formatting), flake8 and pylint (linting), and pytest (automated testing)
- wf_delivery.py     -> Delivery workflow for TestPyPI and PyPI

## Description of typical workflows

__Setting up the project environment__

1. Download or clone the project from GitHub
2. `poetry install`
3. `poetry build`
4. `poetry run peastb --version`

__Developing__

1. Implement new features or fix bugs
2. `poetry run peastb ...`
3. `poetry run pytest tests`

__Testing and Quality assurance__

1. Run the quality workflow with formatting, linting and testing.

__Delivery__

1. Update the version in pyproject.toml
2. Run the delivery workflow without publishing to TestPyPI or PyPI
3. Local installation test with `tox -e local`
4. Run the delivery workflow and publish to TestPyPI
5. Installation test with `tox -e testpypi`
6. Run the delivery workflow and publish to PyPI
7. Installation test with `tox -e pypi`
8. Update git and push to GitHub (`git push`)
9. Tag the version in git and GitHub with an appropriate version string

## Open issues

- (Error) Problem building system after downloading from GitHub on laptop
- (Error) Problem finding executables on Windows after installation with pip
- (New Functionality) Smoke test for scripts
