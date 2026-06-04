import peastb.pea03_analyzer as analyzer


def test_analyze_environment_returns_sections():
    sections = analyzer.analyze_environment()

    assert isinstance(sections, list)
    assert len(sections) == 4

    titles = [section["title"] for section in sections]
    assert "Operating System Information" in titles
    assert "Used Python Information" in titles
    assert "Pip Paths Information" in titles
    assert "Versions" in titles


def test_used_python_section_shape():
    section = analyzer.create_used_python_section()

    assert section["title"] == "Used Python Information"
    assert "Path" in section["content"]
    assert "Version" in section["content"]
