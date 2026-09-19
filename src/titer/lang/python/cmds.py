import shutil
import subprocess
from pathlib import Path


class CommandError(Exception):
    def __init__(
        self,
        command: list[str],
        returncode: int,
        stdout: str = "",
        stderr: str = "",
    ) -> None:
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

        super().__init__(
            f"Command failed with exit code {returncode}"
        )


def run(
    command: list[str],
    cwd: Path | None = None,
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True,
        )

    except subprocess.CalledProcessError as error:
        raise CommandError(
            command=command,
            returncode=error.returncode,
            stdout=error.stdout or "",
            stderr=error.stderr or "",
        ) from error


def uv_init(
    path: Path,
    python_version: str,
) -> None:
    run(
        [
            "uv",
            "init",
            "--no-workspace",
            "--python",
            python_version,
            str(path),
        ]
    )


def uv_venv(
    path: Path,
    python_version: str,
) -> None:
    run(
        [
            "uv",
            "venv",
            "--clear",
            "--python",
            python_version,
        ],
        cwd=path,
    )


def uv_add(
    path: Path,
    dependencies: list[str],
) -> None:
    if not dependencies:
        return

    run(
        [
            "uv",
            "add",
            *dependencies,
        ],
        cwd=path,
    )


def git_init(path: Path) -> None:
    run(
        ["git", "init"],
        cwd=path,
    )


def git_remote_add(
    path: Path,
    name: str,
    url: str,
) -> None:
    run(
        [
            "git",
            "remote",
            "add",
            name,
            url,
        ],
        cwd=path,
    )


def move_main_to_src(path: Path) -> None:
    main = path / "main.py"

    if not main.exists():
        return

    src = path / "src"
    src.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = src / "main.py"

    if destination.exists():
        destination.unlink()

    main.rename(destination)


def install_uv() -> None:
    if shutil.which("uv"):
        return

    run(
        [
            "sh",
            "-c",
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
        ]
    )