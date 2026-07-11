#!/usr/bin/env python3
"""sync_build.py - Development Script for generating version.py with build data and updating readme.md
Name, Organisation:         Markus Breuer, STMB
Created, Last updated:      31.05.2026, 12.06.2026
"""

from datetime import datetime
import toml


def hauptprogramm():
    """Run the main routine that generates version.py."""
    print("Starte Vorbereitung der Build-Phase ...")
    version, _ = versions_datei_erstellen()
    readme_version_aktualisieren(version)
    tox_ini_version_aktualisieren(version)
    print("Build-Phase vorbereitet")


def versions_datei_erstellen():
    """Create version.py with build data from pyproject.toml and the current date."""
    with open("peastb/version.py", "w", encoding="utf-8") as f:
        toml_data = toml.load("pyproject.toml")
        version = toml_data["project"]["version"]
        zeit = datetime.now().strftime("%d.%m.%Y")
        f.write('"""version.py - Build data, generated automatically, do not edit manually\n')
        f.write("Name, Organisation:         Markus Breuer, STMB\n")
        f.write(f"Created, Last updated:      {zeit}, {zeit}\n")
        f.write('"""\n')
        f.write(f"PEASTB_VERSION='{version}'\n")
        f.write(f"PEASTB_VERSION_DATE='{zeit}'\n")
    print(f"1. version.py mit Version {version} und Datum {zeit} erstellt.")
    return version, zeit


def readme_version_aktualisieren(version):
    """Update the version line in README.md."""
    readme_pfad = "README.md"

    with open(readme_pfad, "r", encoding="utf-8") as datei:
        zeilen = datei.readlines()

    aktualisierte_zeilen = []
    versionszeile_gefunden = False

    for zeile in zeilen:
        if zeile.startswith("Current version: "):
            aktualisierte_zeilen.append(f"Current version: {version}\n")
            versionszeile_gefunden = True
        else:
            aktualisierte_zeilen.append(zeile)

    if versionszeile_gefunden:
        with open(readme_pfad, "w", encoding="utf-8") as datei:
            datei.writelines(aktualisierte_zeilen)
        print(f"2. README.md Version auf {version} aktualisiert.")
    else:
        print("2. Hinweis: Keine Versionszeile in README.md gefunden.")


def tox_ini_version_aktualisieren(version):
    """Update the PACKAGE_VERSION line in tox.ini."""
    tox_pfad = "tox.ini"

    with open(tox_pfad, "r", encoding="utf-8") as datei:
        zeilen = datei.readlines()

    aktualisierte_zeilen = []
    versionszeile_gefunden = False

    for zeile in zeilen:
        if zeile.startswith("    PACKAGE_VERSION = "):
            aktualisierte_zeilen.append(f"    PACKAGE_VERSION = {version}\n")
            versionszeile_gefunden = True
        else:
            aktualisierte_zeilen.append(zeile)

    if versionszeile_gefunden:
        with open(tox_pfad, "w", encoding="utf-8") as datei:
            datei.writelines(aktualisierte_zeilen)
        print(f"3. tox.ini Version auf {version} aktualisiert.")
    else:
        print("3. Hinweis: Keine PACKAGE_VERSION-Zeile in tox.ini gefunden.")


if __name__ == "__main__":
    hauptprogramm()
