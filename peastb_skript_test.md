# Skriptprüfung

## TOML Datei

``` toml
[[tools]]
name = "black"
command = ["black", "--version"]

[[tools]]
name = "pytest"
command = ["pytest", "--version"]

[[tools]]
name = "ruff"
command = ["ruff", "--version"]

[[tools]]
name = "uv"
command = ["uv", "--version"]

```

## Code-Fragmente zur Prüfung

### Gesamtvorschlag (danch Modifikationen)

``` python
from pathlib import Path
import shutil
import subprocess


def check_tool(tool_name: str) -> dict:
    result = {
        "name": tool_name,
        "installed": False,
        "version": None,
        "path": None,
        "error": None,
    }

    executable = shutil.which(tool_name)

    if executable is None:
        result["error"] = "nicht gefunden"
        return result

    result["installed"] = True
    result["path"] = executable

    try:
        proc = subprocess.run(
            [tool_name, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        output = (proc.stdout + proc.stderr).strip()
        result["version"] = output.splitlines()[0] if output else "unbekannt"

    except Exception as exc:
        result["error"] = str(exc)

    return result


def load_tools(filename: str):
    return [
        line.strip()
        for line in Path(filename).read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]


if __name__ == "__main__":
    for tool in load_tools("tools.txt"):
        info = check_tool(tool)

        if info["installed"]:
            print(f"[OK] {info['name']}")
            print(f"     Pfad: {info['path']}")
            print(f"     Version: {info['version']}")
        else:
            print(f"[FEHLT] {info['name']}")
```
### Einlesen TOML-Datei

``` python
import tomllib

with open("tools.toml", "rb") as f:
    config = tomllib.load(f)

for tool in config["tools"]:
    print(tool["name"], tool["version_arg"])
```
- Eventuell andere/alte toml verarbeitung

### Prüfbefehle ausführen

``` python
subprocess.run(
    tool["command"],
    capture_output=True,
    text=True,
)
```