import typer
import titer
from rich.console import Console

from . import lang


app = typer.Typer()
console = Console()

printc = console.print


# ─────────────────────────────────────────────
# Colors
# ─────────────────────────────────────────────

colors = {
    "k": "black",
    "r": "red",
    "g": "green",
    "y": "yellow",
    "b": "blue",
    "m": "magenta",
    "c": "cyan",
    "w": "white",

    "o": "#FF8800",
    "p": "#BF00FF",
    "t": "#00E5FF",
    "l": "#39FF14",
    "n": "#FF1493",
    "v": "#8A2BE2",
    "a": "#FFD700",
}


# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────

def check(language: str = "undefined", path: str = ".") -> bool:
    if path is None or path == ".":
        path = "."

    printc(f"{language} path: {path}", style="c")

    if not path:
        path = "."

    from pathlib import Path

    if not Path(path).is_dir():
        printc("Error: path is not a directory", style="r")
        return False

    return True


# ─────────────────────────────────────────────
# Dynamic language loading
# ─────────────────────────────────────────────

def load_languages():
    import importlib
    import pkgutil

    import titer.lang as lang

    def create_command(language_module, language_name):
        def command(
            path: str = typer.Argument("."),
        ):
            if not check(language_name, path):
                return

            language_module.main(path)

        command.__name__ = language_name
        command.__doc__ = (
            f"Initialise un projet {language_name}."
        )

        return command

    for _, name, _ in pkgutil.iter_modules(lang.__path__):
        try:
            language_module = importlib.import_module(
                f"{lang.__name__}.{name}"
            )

            if not hasattr(language_module, "main"):
                continue

            command = create_command(
                language_module,
                name,
            )

            app.command(name=name)(command)

        except Exception as error:
            printc(
                f"Unable to load language '{name}': {error}",
                style="r",
            )


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

@app.callback(invoke_without_command=True)
def main():
    """titer - Initialise facilement des projets."""
    printc(f"Version: {titer.__version__}", style="c")
    printc(f"Author: {titer.__author__}", style="c")
    printc(f"License: {titer.__license__}", style="c")


load_languages()


if __name__ == "__main__":
    app()