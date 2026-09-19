# titer

**titer** is an interactive CLI project generator.

It makes project initialization easier by handling project configuration, dependencies, virtual environments, Git repositories, licenses and project structure through an interactive wizard.

## Features

### Python

The first release focuses on Python projects.

Titer can configure:

- Project name
- Description
- Version
- Author
- Python version
- License
- Virtual environment
- Git repository
- Git remote
- Base dependencies
- Custom dependencies
- `src/` layout

Example:

```bash
titer python ./my-project
````

## Example

```text
$ titer python ./my-project

? Project name: my-project
? Description: My Python project
? Version: 0.1.0
? Author: yolezz
? Python version: 3.13.13
? License: MIT
? Create a virtual environment? Yes
? Initialize Git? Yes
? Link to a remote repository? Yes
? Remote name: origin
? Repository URL: https://github.com/example/my-project.git
? Base dependencies: rich
? Additional dependencies: requests
? Move main.py into src/? Yes

✓ Python project created at /home/user/my-project
```

## Installation

### Debian / Ubuntu

Titer is distributed as a Debian package.

Download the latest `.deb` from the GitHub Releases page and install it with:

```bash
sudo apt install ./titer_1.0.0_amd64.deb
```

Then:

```bash
titer --help
```

The release is compiled with **Nuitka**, so Titer does not require its Python dependencies to be installed separately.

## Development

Requirements:

* Python >= 3.13
* uv
* Git

Clone the repository:

```bash
git clone https://github.com/yolezz/titer.git
cd titer
```

Install the development environment:

```bash
uv sync
```

Run Titer:

```bash
uv run titer --help
```

Generate a project:

```bash
uv run titer python ./my-project
```

## Building

The release build uses **Nuitka** to compile Titer into a standalone executable and then packages it into a Debian package.

Run:

```bash
chmod +x build.sh
./build.sh
```

The resulting package will be:

```text
dist/
└── titer_1.0.0_amd64.deb
```

Install it locally:

```bash
sudo apt install ./dist/titer_1.0.0_amd64.deb
```

## Project structure

```text
titer/
├── src/
│   └── titer/
│       ├── __init__.py
│       ├── __main__.py
│       ├── _metadata.py
│       ├── cli.py
│       └── lang/
│           └── python/
│               ├── __init__.py
│               ├── check.py
│               ├── cmds.py
│               ├── licenses.py
│               ├── main.py
│               ├── pyproject.py
│               └── quest.py
├── build.sh
├── pyproject.toml
├── README.md
└── uv.lock
```

The `lang/` directory contains language-specific project generators.

This allows Titer to support additional languages and ecosystems in future releases.

## Roadmap

### v1.0.0

* [x] Python project generator
* [x] Interactive configuration
* [x] Python version selection
* [x] License selection
* [x] Virtual environment creation
* [x] Dependency management
* [x] Git initialization
* [x] Git remote configuration
* [x] `src/` layout
* [x] Debian package
* [x] Nuitka standalone build

### Future

* [ ] TypeScript / JavaScript
* [ ] Rust
* [ ] More project templates
* [ ] More package managers
* [ ] Additional configuration options

## License

Titer is released under the MIT License.

## Author

Made by **yolezz**.

```