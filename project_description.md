# Project Description

This project has two objectives:

1. It provides a script that analyzes a Python environment.
2. It's a learning project for experimenting with tools, processes, and techniques used in modern Python development.

## Learning Objectives

The following tools are used in this project:

- poetry
- git
- pytest
- tox
- pypi and testpypi

The following techniques have been used in this project:

- Automated component and integration tests with pytest
- System and installation tests with tox and pytest
- Publishing with PyPi and TestPyPi
- Project Versioning and Project Building with Poetry
- Automated Workflows realized with Python scripts: Quality Workflow, Delivery Workflow
- Automated setting of version information based on a single source: pyproject.toml. Realized as a Python script.

## Description of the project directory structure

``` directory structure
SW04_PeaSTB                 -> root directory of the project
├── dev                     -> scripts and tools needed for development
├── dist                    -> distribution directory
├── peastb                  -> Source directory
│   └── __pycache__
├── tests                   -> Component and integration tests; files for pytest
│   └── __pycache__
└── tests_installation      -> Installation tests; files for pytest
    └── __pycache__ 
```

__SW04_PeaSTB (root directory of the project)__

The root directory contains the central configuration and description files.
The root directory is normally the current working directory.
The root directory contains the following files:

- pyproject.toml    ->  Contains the main project configuration for Poetry
- poetry.toml       ->  Contains central Poetry configurations
- poetry.lock       ->  Exact versions of the used packages, automatically maintained by Poetry
- tox.ini           ->  Description of test environments and tests executed by tox (system tests, installation tests)

__dev__

- sync_build.py      ->  Synchronization of version number and build date
- wf_quality.py      ->  Quality workflow using black (formatting), flake8 and pylint (linting) and pytest (automated testing)
- wf_delivery.py     ->  Delivery workflow to TestPyPi and PyPi

## Description of typical workflows

__Setting up the project environment__

1. Download or clone project from github
2. `poetry install`
3. `poetry build`
4. `poetry run peastb --version`

__Developing__

1. Implement new features or fix bugs
2. `poetry run peastb ...`
3. `poetry run pytest tests`

__Testing and Quality assurance__

__Delivery__

1. Update the version in pyproject.toml
2. Delivery workflow without publishing to TestPyPi and PyPi
3. Local installation test with `tox -e local`
4. Delivery workflow with publishing to TestPyPi
5. Installation test with `tox -e testpypi`
6. Delivery workflow with publishing to PyPi
7. Installation test with `tox -e pypi`
8. Update git including `git push` to GitHub
9. Tag the version in git and GitHub with an appropriate version string

## Open issues

- (Error) Problem building system after downloading from github on laptop
- (Error) Problem of finding exexcutables on windows after installation with pip
- (New Functionality) Smoke test for scripts.
