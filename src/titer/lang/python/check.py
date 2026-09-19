import shutil
import subprocess
import sys


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def command_version(command: str) -> str | None:
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        output = result.stdout.strip() or result.stderr.strip()

        return output.splitlines()[0] if output else None

    except (OSError, FileNotFoundError):
        return None


def check_python() -> dict:
    return {
        "installed": True,
        "command": sys.executable,
        "version": (
            f"{sys.version_info.major}."
            f"{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        ),
    }


def check_uv() -> dict:
    installed = command_exists("uv")

    return {
        "installed": installed,
        "command": shutil.which("uv"),
        "version": command_version("uv") if installed else None,
    }


def check_git() -> dict:
    installed = command_exists("git")

    return {
        "installed": installed,
        "command": shutil.which("git"),
        "version": command_version("git") if installed else None,
    }


def uv_python_versions() -> list[dict]:
    if not command_exists("uv"):
        return []

    try:
        result = subprocess.run(
            ["uv", "python", "list", "--only-installed"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return []

    versions = []

    for line in result.stdout.splitlines():
        line = line.strip()

        if not line:
            continue

        # Exemple :
        # cpython-3.13.13-linux-x86_64-gnu
        if line.startswith("cpython-"):
            parts = line.split("-")

            if len(parts) < 2:
                continue

            version = parts[1]

            versions.append(
                {
                    "version": version,
                    "raw": line,
                }
            )

    return versions


def check() -> dict:
    return {
        "python": check_python(),
        "uv": check_uv(),
        "git": check_git(),
        "uv_python_versions": uv_python_versions(),
    }