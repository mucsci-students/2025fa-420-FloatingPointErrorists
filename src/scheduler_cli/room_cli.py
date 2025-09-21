import click
from click_shell import shell
from .base_cli import get_json_config, show, clear, save, run
from .room import Room

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
@shell(prompt="rooms> ", intro="You may now add, modify, or delete rooms.\n Type 'help' to see available commands, 'quit' to exit.\n") # type: ignore
def rooms() -> None:
    """Manage rooms."""
    rooms.add_command(show)
    rooms.add_command(clear)
    rooms.add_command(save)
    rooms.add_command(run)

@rooms.command() # type: ignore
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a room."""
    json_config = get_json_config(ctx)
    rms = [click.prompt("Enter room name", type=str)]
    while click.confirm("Add another?", default=False):
        rms.append(click.prompt("Enter room name", type=str))
    for room in rms:
        try:
            Room.add_room(json_config, room)
        except ValueError as e:
            click.echo(f"{e}")
            rms.remove(room)
    click.echo(f"{rms} added.")

@rooms.command() # type: ignore
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete a room."""
    json_config = get_json_config(ctx)
    room_ids = json_config.scheduler_config.rooms
    if len(room_ids) == 0:
        click.echo("No rooms to delete.")
        return
    rm = click.prompt("Enter room name", type=click.Choice(room_ids), show_default=False, show_choices=False)
    Room.del_room(json_config, rm)
    click.echo(f"{rm} deleted.")
    while click.confirm("Delete another?", default=False):
        rm = click.prompt("Enter room name", type=click.Choice(room_ids), show_default=False, show_choices=False)
        Room.del_room(json_config, rm)
        click.echo(f"{rm} deleted.")

@rooms.command() # type: ignore
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify a room."""
    json_config = get_json_config(ctx)
    room_ids = json_config.scheduler_config.rooms
    if len(room_ids) == 0:
        click.echo("No rooms to modify.")
        return
    rm = click.prompt("Enter room name to modify", type=click.Choice(room_ids), show_default=False, show_choices=False)
    rm2 = click.prompt("New room name", type=str)
    Room.mod_room(json_config, rm, rm2)
    click.echo(f"{rm} is now {rm2}.")