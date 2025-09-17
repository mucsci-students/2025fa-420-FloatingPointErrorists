import click
from click_shell import shell
from .json import JsonConfig

"""
This module implements a command-line interface (CLI) for managing JSON configuration files.
It allows users to load, view, and save configurations interactively.

The ctx.obj dictionary is used to store the current configuration state across different commands.
To utilize it for a command:

1- Ensure @click.pass_context is above the command function definition.
2- Add a parameter ctx: click.Context to the command function.
3- If you want to add something to the context object, use ctx.obj[key] = value.

To read up on how to use click, visit: https://click.palletsprojects.com/en/stable/
"""

CONFIG_KEY = "config"

# ====== CLI Definition & General functions ======
@shell(prompt="scheduler> ", intro="Welcome to the Scheduler CLI!\nType 'help' to see available commands, 'quit' to exit.\n")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Scheduler CLI — interactive shell."""
    ctx.ensure_object(dict)

def run_shell() -> None:
    """Run the interactive shell."""
    cli()

def handle_sigint(signum, frame):
    """Handle SIGINT (Ctrl+C) signal."""
    import sys
    click.echo("\nExiting on user interrupt (Ctrl+C).")
    sys.exit(130)  # 130 is the conventional exit code for SIGINT

def apply_signal_handlers():
    """Apply signal handlers for graceful shutdown."""
    import signal
    signal.signal(signal.SIGINT, handle_sigint)

# ====== JSON Commands ======
@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_context
def load(ctx: click.Context, file_path: str) -> None:
    """Load a JSON configuration file."""
    import json
    try:
        config = JsonConfig(file_path)
        ctx.obj[CONFIG_KEY] = config
        click.echo("Configuration loaded")
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")

@cli.command()
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show the loaded configuration."""
    config = ctx.obj.get(CONFIG_KEY)
    if not config:
        click.echo("No configuration loaded.")
    else:
        click.echo(config)

@cli.command()
@click.pass_context
def save(ctx: click.Context) -> None:
    """Save the current configuration back to the file."""
    try:
        config = ctx.obj.get(CONFIG_KEY)
        if not config:
            click.echo("No configuration loaded.")
        else:
            config.save()
            click.echo("Configuration saved.")
    except PermissionError as e:
        raise click.ClickException(f"Permission error: {e}")
