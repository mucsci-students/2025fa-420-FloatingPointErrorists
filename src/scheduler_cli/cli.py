import click
import shlex
import json
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

@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Scheduler CLI — interactive shell."""
    ctx.ensure_object(dict)

@cli.command("load")
@click.argument("file-path", type=click.Path(exists=True))
@click.pass_context
def load(ctx: click.Context, file_path: str) -> None:
    """Load a JSON configuration file."""
    try:
        config = JsonConfig(file_path)
        ctx.obj[CONFIG_KEY] = config
        click.echo("Configuration loaded")
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")

@cli.command("room")
@click.pass_context
def room(ctx: click.Context) -> None:
    """Modify the rooms of a configuration"""
    config = ctx.obj.get(CONFIG_KEY)
    if not config:
        click.echo("No configuration loaded.")
    else:
        click.echo(config)

@cli.command("lab")
@click.pass_context
def room(ctx: click.Context) -> None:
    """Modify the labs of a configuration"""
    config = ctx.obj.get(CONFIG_KEY)
    if not config:
        click.echo("No configuration loaded.")
    else:
        click.echo(config)

@cli.command("show")
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show the loaded configuration."""
    config = ctx.obj.get(CONFIG_KEY)
    if not config:
        click.echo("No configuration loaded.")
    else:
        click.echo(config)

@cli.command("save")
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
        click.ClickException(f"Permission error: {e}")

@cli.command("quit")
def quit_program() -> None:
    """Exit the program."""
    raise SystemExit

def run_shell() -> None:
    click.echo("Welcome to the Scheduler CLI!")
    click.echo("Type 'help' to see available commands, 'quit' to exit.\n")
    ctx = click.Context(cli)
    ctx.ensure_object(dict)
    while True:
        try:
            raw_input = input("scheduler> ").strip()
            if not raw_input:
                continue
            if raw_input == "help":
                click.echo(cli.get_help(click.Context(cli)))
                continue
            args = shlex.split(raw_input)
            cli.main(args=args, prog_name="scheduler", standalone_mode=False, obj=ctx.obj)
        except SystemExit:
            break
        except KeyboardInterrupt:
            click.echo("\nExiting on user interrupt (Ctrl+C).")
            break
        except Exception as e:
            click.echo(f"{e}")
