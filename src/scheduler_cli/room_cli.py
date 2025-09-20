import click
from click_shell import shell
from .base_cli import get_json_config, show

"""
This module implements a command-line interface (CLI) for managing rooms in the configuration file.
It allows users to add, modify and delete rooms.

The ctx.obj dictionary is used to store the current configuration state across different commands.
To utilize it for a command:

1- Ensure @click.pass_context is above the command function definition.
2- Add a parameter ctx: click.Context to the command function.
3- If you want to add something to the context object, use ctx.obj[key] = value.

To read up on how to use click, visit: https://click.palletsprojects.com/en/stable/
"""

# ===== Rooms shell =====
@shell(prompt="Rooms> ", intro="You may now add, modify, or delete rooms.\n Type 'help' to see available commands, 'quit' to exit.\n") # type: ignore
def rooms() -> None:
    """Manage rooms."""
    rooms.add_command(show)


@rooms.command()
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a room."""
    json_config = get_json_config(ctx)
    rms = []
    rms.append(click.prompt("Enter room name", type=str))
    while click.confirm("Add another?", default=False):
        rms.append(click.prompt("Enter room name", type=str))
    for room in rms:
        room.add_room(json_config, rms)
    click.echo(f"{rms} added.")

@rooms.command()
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete a room."""
    json_config = get_json_config(ctx)
    room_ids = [room for room in json_config.scheduler_config.rooms]
    rm = click.prompt("Enter room name", type=click.Choice(room_ids), show_default=False)
    room.delete_room(rm)
    click.echo(f"{rm} deleted.")
    while click.confirm("Delete another?", default=False):
        rm = click.prompt("Enter room name", type=click.choice(room_ids), show_default=False)
        room.delete_room(json_config, rm)
        click.echo(f"{rm} deleted.")

@rooms.command()
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify a room."""
    json_config = get_json_config(ctx)
    room_ids = [room for room in json_config.scheduler_config.rooms]
    rm = click.prompt("Enter room name to modify", type=click.choice(room_ids), show_default=False)
    rm2 = click.prompt("New room name", type=str)
    room.modify_room(json_config, rm, rm2)
    click.echo(f"{rm} is now {rm2}")