""" sync_build.py - Das Skript erzeugt eine version.py mit den Build-Daten 
    Name, Organisaion:          Markus Breuer, STMB
    Erstellt, Letzte Änderung:  31.05.2026
    """


from datetime import datetime
import toml


def hauptprogramm():
    """Hauptprogramm des Skripts, das die version.py erstellt """
    print("Starte Vorbereitung der Build-Phase ...")
    version, _ = versions_datei_erstellen()
    readme_version_aktualisieren(version)
    print("Build-Phase vorbereitet")


def versions_datei_erstellen():
    """Erstellt die version.py mit den Build-Daten; Verion aus pyproject.toml, Datum aus aktuellem Zeitpunkt"""
    with open("peastb/version.py", "w") as f:
        toml_data = toml.load("pyproject.toml")
        version = toml_data["project"]["version"]
        zeit = datetime.now().strftime("%d.%m.%Y")
        f.write(f"# Build Data, automatisch generiert, nicht manuell ändern!\n")
        f.write(f"PEASTB_VERSION='{version}'\n")
        f.write(f"PEASTB_VERSION_DATE='{zeit}'\n")
    print(f"1. version.py mit Version {version} und Datum {zeit} erstellt.")
    return version, zeit


def readme_version_aktualisieren(version):
    """Aktualisiert die Versionszeile in der README.md."""
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


if __name__ == "__main__":
    hauptprogramm()
