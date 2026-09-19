from datetime import datetime
from pathlib import Path
import urllib.request

import questionary
from rich.console import Console

from . import cmds
from .check import check
from .licenses import LICENSES
from .pyproject import update as update_pyproject
from .quest import ask_all


console = Console()


def handle_command_error(
    error: cmds.CommandError,
) -> None:
    command = " ".join(error.command)

    console.print(
        f"[red]✗ Command failed:[/red] {command}"
    )

    output = error.stderr.strip()

    if not output:
        output = error.stdout.strip()

    if output:
        console.print()
        console.print(output)

    console.print(
        f"\n[dim]Exit code: {error.returncode}[/dim]"
    )


def clear_directory(path: Path) -> None:
    for item in path.iterdir():
        if item.is_dir() and not item.is_symlink():
            import shutil

            shutil.rmtree(item)
        else:
            item.unlink()


def download_license(
    path: Path,
    license_id: str,
    author: str,
) -> None:
    license_data = LICENSES[license_id]
    url = license_data["url"]

    try:
        license_path = path / "LICENSE"

        urllib.request.urlretrieve(
            url,
            license_path,
        )

        content = license_path.read_text(
            encoding="utf-8",
        )

        content = content.replace(
            "<year>",
            str(datetime.now().year),
        )

        content = content.replace(
            "<owner>",
            author,
        )

        license_path.write_text(
            content,
            encoding="utf-8",
        )

    except Exception as error:
        console.print(
            f"[yellow]Warning:[/yellow] "
            f"unable to download "
            f"the {license_id} license: {error}"
        )


def update_readme(
    path: Path,
    name: str,
    description: str,
) -> None:
    readme = path / "README.md"

    content = f"# {name}\n"

    if description.strip():
        content += f"\n{description}\n"

    readme.write_text(
        content,
        encoding="utf-8",
    )


def ensure_uv() -> bool:
    if cmds.shutil.which("uv"):
        return True

    console.print(
        "[yellow]✗ uv is not installed.[/yellow]"
    )

    install = questionary.confirm(
        "Install uv now?",
        default=True,
    ).ask()

    if not install:
        console.print(
            "[red]Cannot continue without uv.[/red]"
        )
        return False

    console.print(
        "[cyan]Installing uv...[/cyan]"
    )

    try:
        cmds.install_uv()
    except cmds.CommandError as error:
        handle_command_error(error)
        return False

    if not cmds.shutil.which("uv"):
        console.print(
            "[red]uv installation completed, "
            "but uv was not found in PATH.[/red]"
        )

        console.print(
            "[yellow]Restart your shell and try again.[/yellow]"
        )

        return False

    console.print(
        "[green]✓ uv installed.[/green]"
    )

    return True


def main(path: str) -> None:
    path = Path(path).resolve()

    console.print(
        f"[dim]python path: {path}[/dim]"
    )

    if not ensure_uv():
        return

    if not path.exists():
        path.mkdir(
            parents=True,
            exist_ok=True,
        )

    if not path.is_dir():
        console.print(
            f"[red]✗ Path is not a directory:[/red] "
            f"{path}"
        )
        return

    if any(path.iterdir()):
        clear = questionary.confirm(
            "Directory is not empty. "
            "Clear it and continue?",
            default=False,
        ).ask()

        if not clear:
            console.print(
                "[yellow]Aborted.[/yellow]"
            )
            return

        try:
            clear_directory(path)
        except Exception as error:
            console.print(
                f"[red]✗ Failed to clear directory:[/red] "
                f"{error}"
            )
            return

    environment = check()

    uv = environment["uv"]
    git = environment["git"]
    python = environment["python"]
    python_versions = environment["uv_python_versions"]

    if not uv["installed"]:
        console.print(
            "[red]uv is not available.[/red]"
        )
        return

    config = ask_all(
        default_name=path.name,
        python_versions=python_versions,
        current_python=python["version"],
    )

    try:
        cmds.uv_init(
            path,
            config["python"],
        )
    except cmds.CommandError as error:
        handle_command_error(error)
        return

    update_pyproject(
        path,
        name=config["name"],
        description=config["description"],
        version=config["version"],
        author=config["author"],
        python_version=config["python"],
        license_id=config["license"],
    )

    update_readme(
        path,
        config["name"],
        config["description"],
    )

    if config["src"]:
        try:
            cmds.move_main_to_src(path)
        except Exception as error:
            console.print(
                f"[red]✗ Failed to move main.py:[/red] "
                f"{error}"
            )
            return

    if config["venv"]:
        try:
            cmds.uv_venv(
                path,
                config["python"],
            )
        except cmds.CommandError as error:
            handle_command_error(error)
            return

    if config["dependencies"]:
        try:
            cmds.uv_add(
                path,
                config["dependencies"],
            )
        except cmds.CommandError as error:
            handle_command_error(error)
            return

    if config["git"]:
        if not git["installed"]:
            console.print(
                "[yellow]Warning:[/yellow] "
                "Git is not installed. "
                "Skipping Git initialization."
            )
        else:
            try:
                cmds.git_init(path)
            except cmds.CommandError as error:
                handle_command_error(error)
                return

            if config["git_remote"]:
                if not config["git_remote_url"].strip():
                    console.print(
                        "[yellow]Warning:[/yellow] "
                        "Repository URL is empty. "
                        "Skipping remote."
                    )
                else:
                    try:
                        cmds.git_remote_add(
                            path,
                            config["git_remote_name"],
                            config["git_remote_url"],
                        )
                    except cmds.CommandError as error:
                        handle_command_error(error)
                        return

    if config["license"]:
        download_license(
            path,
            config["license"],
            config["author"],
        )

    console.print()
    console.print(
        f"[green]✓[/green] "
        f"Python project created at {path}"
    )