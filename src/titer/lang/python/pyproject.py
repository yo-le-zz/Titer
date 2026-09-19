from pathlib import Path

import tomlkit


def update(
    path: Path,
    *,
    name: str,
    description: str,
    version: str,
    author: str,
    python_version: str,
    license_id: str | None,
) -> None:
    pyproject_path = path / "pyproject.toml"

    with pyproject_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        document = tomlkit.load(file)

    project = document["project"]

    project["name"] = name
    project["version"] = version
    project["description"] = description
    project["requires-python"] = f">={python_version}"

    if author.strip():
        author_table = tomlkit.inline_table()
        author_table["name"] = author.strip()

        authors = tomlkit.array()
        authors.append(author_table)

        project["authors"] = authors
    else:
        project.pop("authors", None)

    if license_id:
        project["license"] = license_id
    else:
        project.pop("license", None)

    with pyproject_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        tomlkit.dump(document, file)