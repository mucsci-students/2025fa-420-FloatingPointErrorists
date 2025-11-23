import sys

import click

from .cli import apply_signal_handlers, base_cli


def run_shell() -> None:
    """
    Apply signal handlers and run the base CLI shell.
    This function modifies sys.argv to remove the '--cli' argument if present,
    because the shell for base_cli does not expect it.
    """
    apply_signal_handlers()
    argv_backup = sys.argv.copy()
    try:
        sys.argv = [arg for arg in sys.argv if arg != "--cli"]
        base_cli()
    finally:
        sys.argv = argv_backup


@click.command()
@click.option("--cli", is_flag=True, help="Run in CLI mode.")
def main(cli: bool) -> None:
    if cli:
        run_shell()
    else:
        try:
            from .view import view

            view()
        except ImportError:
            click.echo(
                "GUI dependencies are not installed. Please install the required packages to run the GUI."
            )
