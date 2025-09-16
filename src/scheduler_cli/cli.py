import json
import click
from click_shell import shell
from .json import JsonConfig

"""
This module implements a command-line interface (CLI) for managing JSON configuration files.
It allows users to load, view, and save configurations interactively.

The ctx.obj dictionary is used to store the current configuration state across different commands.
"""

CONFIG_KEY = "config"

# Main interactive shell
@shell(prompt="scheduler> ", intro="Welcome to the Scheduler CLI!\nType 'help' to see available commands, 'exit' to exit.\n")
def cli() -> None:
    """Scheduler CLI — interactive shell."""
    ctx = click.Context(cli)
    ctx.ensure_object(dict)

@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_context
def load(ctx: click.Context, file_path: str) -> None:
    """Load a JSON configuration file."""
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