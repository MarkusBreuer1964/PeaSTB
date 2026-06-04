import peastb.pea04_output as output_service


def test_build_report_includes_intro_and_sections():
    title_information = {
        "title": "Python Environment Analyzer (PeaSTB)",
        "date": "2026-06-03 20:00:00",
        "computer_name": "demo-machine",
        "user_name": "demo-user",
        "peastb_version": "0.1.0a2",
        "peastb_version_date": "04.06.2026",
    }
    sections = [
        {
            "title": "Example Section",
            "content": {"Key": "Value"},
        }
    ]

    report = output_service.build_report(title_information, sections)

    assert "Python Environment Analyzer (PeaSTB)" in report
    assert "Date" in report
    assert "Computer name" in report
    assert "User name" in report
    assert "PeaSTB version" in report
    assert "PeaSTB Version Date" in report
    assert "0.1.0a2" in report
    assert "04.06.2026" in report
    assert "Example Section" in report
    assert "Key" in report
    assert "Value" in report
