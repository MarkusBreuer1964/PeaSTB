import peastb.pea02_package_check as package_check


def test_run_package_check_returns_detail_and_summary_sections(tmp_path):
    package_file = tmp_path / "packages.txt"
    package_file.write_text("sys\nthis_package_should_not_exist_123\n", encoding="utf-8")

    sections = package_check.run_package_check(str(package_file))

    assert len(sections) == 3
    detail_section = sections[0]
    summary_section = sections[1]
    installed_packages_section = sections[2]

    assert detail_section["title"] == "Package Import Check (importlib.import_module)"
    assert detail_section["content"]["sys"] == "successful"
    assert detail_section["content"]["this_package_should_not_exist_123"] == "not successful"

    assert summary_section["title"] == "Package Import Summary (count)"
    assert summary_section["content"]["Successful Imports"] == 1
    assert summary_section["content"]["Failed Imports"] == 1

    assert installed_packages_section["title"] == "Installed Packages (pip list --verbose)"
    assert len(installed_packages_section["content"]) > 0

    first_value = next(iter(installed_packages_section["content"].values()))
    assert " -> " in first_value


def test_load_package_list_raises_for_empty_file(tmp_path):
    package_file = tmp_path / "packages.txt"
    package_file.write_text("# comment only\n\n", encoding="utf-8")

    try:
        package_check.load_package_list_from_file(str(package_file))
        assert False, "ValueError expected"
    except ValueError as exc:
        assert "does not contain any packages" in str(exc)


def test_run_package_check_without_packagefile_returns_installed_packages_section():
    sections = package_check.run_package_check()

    assert len(sections) == 1
    installed_packages_section = sections[0]

    assert installed_packages_section["title"] == "Installed Packages (pip list --verbose)"
    assert len(installed_packages_section["content"]) > 0

    first_value = next(iter(installed_packages_section["content"].values()))
    assert " -> " in first_value
