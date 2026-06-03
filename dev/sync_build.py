""" sync_build.py - Das Skript erzeugt eine version.py mit den Build-Daten 
    Name, Organisaion:          Markus Breuer, STMB
    Erstellt, Letzte Änderung:  31.05.2026
    """


from datetime import datetime
import toml


def hauptprogramm():
    """Hauptprogramm des Skripts, das die version.py erstellt """
    print("Starte Vorbereitung der Build-Phase ...")
    versions_datei_erstellen()
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


if __name__ == "__main__":
    hauptprogramm()
