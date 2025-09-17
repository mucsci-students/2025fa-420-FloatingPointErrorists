import click
import types
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

CONFIG_KEY: str = "config"
NO_CONFIG_LOADED: str = "No configuration loaded. Please load a configuration first."

# ====== CLI Definition & General functions ======
@shell(prompt="scheduler> ", intro="Welcome to the Scheduler CLI!\nType 'help' to see available commands, 'quit' to exit.\n") # type: ignore
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Scheduler CLI — interactive shell."""
    ctx.ensure_object(dict)
    cli.add_command(faculty)

def run_shell() -> None:
    """Run the interactive shell."""
    cli()

def handle_sigint(signum: int, frame: types.FrameType | None) -> None:
    """Handle SIGINT (Ctrl+C) signal."""
    import sys
    click.echo("\nExiting on user interrupt (Ctrl+C).")
    sys.exit(0)

def apply_signal_handlers() -> None:
    """Apply signal handlers for graceful shutdown."""
    import signal
    signal.signal(signal.SIGINT, handle_sigint)

# ====== JSON Commands ======
@cli.command() # type: ignore
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

@cli.command() # type: ignore
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show the loaded configuration."""
    config = ctx.obj.get(CONFIG_KEY)
    if not config:
        click.echo(NO_CONFIG_LOADED)
    else:
        click.echo(config)

@cli.command() # type: ignore
@click.pass_context
def save(ctx: click.Context) -> None:
    """Save the current configuration back to the file."""
    try:
        config = ctx.obj.get(CONFIG_KEY)
        if not config:
            click.echo(NO_CONFIG_LOADED)
        else:
            config.save()
            click.echo("Configuration saved.")
    except PermissionError as e:
        raise click.ClickException(f"Permission error: {e}")

# ===== Faculty shell =====
@shell(prompt="faculty> ", intro="You may now add, modify, or delete faculty.\nType 'help' to see available commands, 'exit' to return to main shell.\n") # type: ignore
@click.pass_context
def faculty(ctx: click.Context) -> None:
    """Manage faculty"""
    config = ctx.obj.get(CONFIG_KEY)
    if not config:
        click.echo(NO_CONFIG_LOADED)
        ctx.exit(1)

@faculty.command() # type: ignore
@click.pass_context
def add(ctx: click.Context) -> None:
    name = click.prompt("Faculty member's name")
    maximum_credits = click.prompt("Maximum credit hours", type=int)
    minimum_credits = click.prompt("Minimum credit hours", type=int)
    unique_course_limit = click.prompt("Unique course limit", type=int)


@faculty.command() # type: ignore
@click.argument("name")
def delete(name: str) -> None:
    click.echo(f"Faculty '{name}' deleted.")


@faculty.command() # type: ignore
@click.argument("old_name")
@click.argument("new_name")
def modify(old_name: str, new_name: str) -> None:
    click.echo(f"Faculty '{old_name}' renamed to '{new_name}'.")