import peastb.pea03_analyzer as analyzer


def test_analyze_environment_returns_sections():
    sections = analyzer.analyze_environment()

    assert isinstance(sections, list)
    assert len(sections) == 8

    titles = [section["title"] for section in sections]
    assert "Operating System Information" in titles
    assert "Used Python Information" in titles
    assert "Environment Paths" in titles
    assert "Pip Executable Paths" in titles
    assert "Version Information" in titles
    assert "Module Search Paths" in titles
    assert "Site Packages Paths" in titles
    assert "Virtual Environment Status" in titles


def test_used_python_section_shape():
    section = analyzer.create_used_python_section()

    assert section["title"] == "Used Python Information"
    assert "Path" in section["content"]
    assert "Version" in section["content"]


def test_environment_paths_section_shape():
    section = analyzer.create_environment_paths_section()

    assert section["title"] == "Environment Paths"
    assert "Python Reachable" in section["content"]
    assert "Python Paths" in section["content"]
    assert "Pip Reachable" in section["content"]
    assert "Pip Paths" in section["content"]


def test_module_search_paths_section_shape():
    section = analyzer.create_module_search_paths_section()

    assert section["title"] == "Module Search Paths"
    assert len(section["content"]) > 0


def test_site_packages_section_shape():
    section = analyzer.create_site_packages_section()

    assert section["title"] == "Site Packages Paths"
    assert len(section["content"]) > 0


def test_virtual_environment_section_shape():
    section = analyzer.create_virtual_environment_section()

    assert section["title"] == "Virtual Environment Status"
    assert "Virtual Environment Status" in section["content"]
    assert "Virtual Environment Path" in section["content"]
    assert "Base Prefix" in section["content"]
