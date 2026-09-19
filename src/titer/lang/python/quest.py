import questionary

from .licenses import LICENSES


BASE_DEPENDENCIES = [
    "rich",
    "requests",
    "typer",
    "questionary",
]


def ask_text(message: str, default: str = "") -> str:
    return questionary.text(
        message,
        default=default,
    ).ask()


def ask_confirm(message: str, default: bool = True) -> bool:
    return questionary.confirm(
        message,
        default=default,
    ).ask()


def ask_project_name(default: str) -> str:
    return ask_text(
        "Project name:",
        default=default,
    )


def ask_description() -> str:
    return ask_text(
        "Description:",
        default="",
    )


def ask_version() -> str:
    return ask_text(
        "Version:",
        default="0.1.0",
    )


def ask_author() -> str:
    return ask_text(
        "Author:",
        default="",
    )


def ask_python_version(
    versions: list[dict],
    current_version: str,
) -> str:
    choices = []

    for python in versions:
        choices.append(
            questionary.Choice(
                python["version"],
                value=python["version"],
            )
        )

    if current_version not in [
        python["version"]
        for python in versions
    ]:
        choices.insert(
            0,
            questionary.Choice(
                f"{current_version} (system)",
                value=current_version,
            ),
        )

    return questionary.select(
        "Python version:",
        choices=choices,
        default=current_version,
    ).ask()


def ask_license() -> str | None:
    choices = [
        questionary.Choice(
            license_data["name"],
            value=spdx,
        )
        for spdx, license_data in LICENSES.items()
    ]

    choices.append(
        questionary.Choice(
            "No license",
            value=None,
        )
    )

    return questionary.select(
        "License:",
        choices=choices,
    ).ask()


def ask_venv() -> bool:
    return ask_confirm(
        "Create a virtual environment?",
        default=True,
    )


def ask_git() -> bool:
    return ask_confirm(
        "Initialize Git?",
        default=True,
    )


def ask_git_remote() -> bool:
    return ask_confirm(
        "Link to a remote repository?",
        default=False,
    )


def ask_git_remote_name() -> str:
    return ask_text(
        "Remote name:",
        default="origin",
    )


def ask_git_remote_url() -> str:
    return ask_text(
        "Repository URL:",
        default="",
    )


def ask_src() -> bool:
    return ask_confirm(
        "Move main.py into src/?",
        default=False,
    )


def ask_dependencies() -> list[str]:
    selected = questionary.checkbox(
        "Base dependencies:",
        choices=BASE_DEPENDENCIES,
    ).ask()

    custom = questionary.text(
        "Additional dependencies "
        "(comma separated, empty to skip):",
        default="",
    ).ask()

    if custom.strip():
        selected.extend(
            dependency.strip()
            for dependency in custom.split(",")
            if dependency.strip()
        )

    return list(dict.fromkeys(selected))


def ask_all(
    default_name: str,
    python_versions: list[dict],
    current_python: str,
) -> dict:
    config = {
        "name": ask_project_name(default_name),
        "description": ask_description(),
        "version": ask_version(),
        "author": ask_author(),
        "python": ask_python_version(
            python_versions,
            current_python,
        ),
        "license": ask_license(),
        "venv": ask_venv(),
        "git": ask_git(),
        "git_remote": False,
        "git_remote_name": "origin",
        "git_remote_url": "",
        "src": False,
        "dependencies": ask_dependencies(),
    }

    if config["git"]:
        config["git_remote"] = ask_git_remote()

        if config["git_remote"]:
            config["git_remote_name"] = ask_git_remote_name()
            config["git_remote_url"] = ask_git_remote_url()

    config["src"] = ask_src()

    return config