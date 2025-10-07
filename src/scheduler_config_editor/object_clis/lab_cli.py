import click
from click_shell import shell
from scheduler_config_editor.base_cli import get_json_config, show, clear, save, run
from scheduler_config_editor.model.lab import Lab

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

# ===== Labs shell =====
@shell(prompt="labs> ", intro="You may now add, modify, or delete labs.\n Type 'help' to see available commands, 'quit' to exit.\n") # type: ignore
def labs() -> None:
    """Manage rooms."""
    labs.add_command(show)
    labs.add_command(clear)
    labs.add_command(save)
    labs.add_command(run)

@labs.command()  # type: ignore
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a lab."""
    json_config = get_json_config(ctx)
    lab_list = [click.prompt("Enter lab name", type=str)]
    while click.confirm("Add another?", default=False):
        lab_list.append(click.prompt("Enter lab name", type=str))
    for lb in lab_list:
        try:
            Lab.add_lab(json_config, lb)
        except ValueError as e:
            click.echo(f"{e}")
            lab_list.remove(lb)
    click.echo(f"Added {lab_list}.")

@labs.command()  # type: ignore
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete a lab."""
    json_config = get_json_config(ctx)
    lab_ids = json_config.scheduler_config.labs
    if len(lab_ids) == 0:
        click.echo("No labs to delete.")
        return
    lb = click.prompt("Enter lab name", type=click.Choice(lab_ids), show_choices=False)
    Lab.del_lab(json_config, lb)
    click.echo(f"{lb} deleted")
    while click.confirm("Delete another?", default=False):
        lb = click.prompt("Enter lab name", type=click.Choice(lab_ids), show_choices=False)
        Lab.del_lab(json_config, lb)
        click.echo(f"{lb} deleted.")

@labs.command()  # type: ignore
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify a lab."""
    json_config = get_json_config(ctx)
    lab_ids = json_config.scheduler_config.labs
    if len(lab_ids) == 0:
        click.echo("No labs to modify.")
        return
    lb = click.prompt("Enter lab name to modify", type=click.Choice(lab_ids), show_choices=False)
    lb2 = click.prompt("New lab name", type=str)
    Lab.mod_lab(json_config, lb, lb2)
    click.echo(f"{lb} is now {lb2}.")