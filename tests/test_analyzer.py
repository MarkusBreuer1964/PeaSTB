import peastb.pea03_analyzer as analyzer


def test_analyze_environment_returns_sections():
    sections = analyzer.analyze_environment()

    assert isinstance(sections, list)
    assert len(sections) == 9

    titles = [section["title"] for section in sections]
    assert "Operating System Information (platform)" in titles
    assert "Used Python Information (sys.executable, platform.python_version)" in titles
    assert "Environment Paths (which/where)" in titles
    assert "Pip Executable Paths (shutil.which)" in titles
    assert "Version Information (--version)" in titles
    assert "Module Search Paths (sys.path)" in titles
    assert "Site Packages Paths (site.getsitepackages)" in titles
    assert "User Site Packages Paths (site.getusersitepackages)" in titles
    assert "Virtual Environment Status (sys.prefix vs sys.base_prefix)" in titles


def test_used_python_section_shape():
    section = analyzer.create_used_python_section()

    assert section["title"] == "Used Python Information (sys.executable, platform.python_version)"
    assert "Path" in section["content"]
    assert "Version" in section["content"]


def test_environment_paths_section_shape():
    section = analyzer.create_environment_paths_section()

    assert section["title"] == "Environment Paths (which/where)"
    assert "Python Reachable" in section["content"]
    assert "Python Paths" in section["content"]
    assert "Pip Reachable" in section["content"]
    assert "Pip Paths" in section["content"]


def test_module_search_paths_section_shape():
    section = analyzer.create_module_search_paths_section()

    assert section["title"] == "Module Search Paths (sys.path)"
    assert len(section["content"]) > 0


def test_site_packages_section_shape():
    section = analyzer.create_site_packages_section()

    assert section["title"] == "Site Packages Paths (site.getsitepackages)"
    assert len(section["content"]) > 0


def test_virtual_environment_section_shape():
    section = analyzer.create_virtual_environment_section()

    assert section["title"] == "Virtual Environment Status (sys.prefix vs sys.base_prefix)"
    assert "Virtual Environment Status" in section["content"]
    assert "Virtual Environment Path" in section["content"]
    assert "Base Prefix" in section["content"]


def test_user_site_packages_section_shape():
    section = analyzer.create_user_site_packages_section()

    assert section["title"] == "User Site Packages Paths (site.getusersitepackages)"
    assert "User Site Package Path" in section["content"]
