import click
import types
import os
import signal
from click_shell import shell
from scheduler import OptimizerFlags
from scheduler.json_types import CourseInstanceJSON
from scheduler_config_editor.model.schedule_handler import ScheduleHandler
from scheduler_config_editor.model.json import JsonConfig
from scheduler_config_editor.model.run_scheduler import run_using_config, write_as_json, write_as_csv

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

HANDLER_KEY = "SCHEDULER_CLI_HANDLER"

# ====== CLI Definition & General functions ======
@shell(prompt="scheduler> ", intro="Welcome to the Scheduler CLI!\nType 'help' to see available commands, 'quit' to exit.\n") # type: ignore
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Scheduler CLI — interactive shell."""
    ctx.ensure_object(dict)

def handle_sigint(signum: int, frame: types.FrameType | None) -> None:
    """Handle SIGINT (Ctrl+C) signal."""
    click.echo("\nExiting on user interrupt (Ctrl+C).")
    raise SystemExit

def apply_signal_handlers() -> None:
    """Apply signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, handle_sigint)

def get_json_config(ctx: click.Context) -> JsonConfig:
    """Helper function to get the current JSON configuration."""
    config: JsonConfig = ctx.obj.get("config")
    if not config:
        raise click.ClickException("No configuration loaded. Please do 'load <configuration>' first.")
    return config

def enable_configuration_commands() -> None:
    """Add all the sub-shells to the cli."""
    from .faculty_cli import faculty
    from .course_cli import courses
    from .room_cli import rooms
    from .lab_cli import labs
    cli.add_command(faculty)  # Add faculty sub-shell
    cli.add_command(courses)  # Add courses sub-shell
    cli.add_command(rooms)  # Add rooms sub-shell
    cli.add_command(labs)  # Add labs sub-shell

def check_valid_config(json_config: JsonConfig) -> None:
    """Check if a valid configuration is loaded."""
    config = json_config.scheduler_config
    if len(config.rooms) == 0:
        raise click.ClickException("No rooms defined in the configuration.")
    if len(config.labs) == 0:
        raise click.ClickException("No labs defined in the configuration.")
    if len(config.faculty) == 0:
        raise click.ClickException("No faculty defined in the configuration.")
    if len(config.courses) == 0:
        raise click.ClickException("No courses defined in the configuration.")

@cli.command() # type: ignore
def clear() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

# ====== JSON Commands ======
@cli.command() # type: ignore
@click.argument("file_path", type=click.Path())
@click.pass_context
def load_config(ctx: click.Context, file_path: str) -> None:
    """Load a JSON configuration file."""
    import json
    try:
        config = JsonConfig(file_path)
        ctx.obj["config"] = config
        enable_configuration_commands()
        click.echo("Configuration loaded")
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")

@cli.command() # type: ignore
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show the loaded configuration."""
    config = get_json_config(ctx)
    click.echo(config)

@cli.command() # type: ignore
@click.pass_context
def save(ctx: click.Context) -> None:
    """Save the current configuration back to the file."""
    try:
        config = get_json_config(ctx)
        config.save()
        click.echo("Configuration saved.")
    except PermissionError as e:
        raise click.ClickException(f"Permission error: {e}")

@cli.command() # type: ignore
@click.argument("file_path", type=click.Path())
@click.pass_context
def load_schedules(ctx: click.Context, file_path: str) -> None:
    """Load schedules from a JSON or CSV file."""
    try:
        schedule_handler = ScheduleHandler()
        schedule_handler.import_schedules(file_path)
        schedules = schedule_handler.schedules
        if not schedules:
            click.echo("No schedules found in the file.")
            return
        ctx.obj[HANDLER_KEY] = schedule_handler
        from .schedule_viewer import schedule_viewer
        cli.add_command(schedule_viewer)
        schedule_viewer.main(standalone_mode=False, obj=ctx.obj)
    except FileNotFoundError as e:
        raise click.ClickException(f"{e}")

@cli.command() # type: ignore
@click.pass_context
def run(ctx: click.Context) -> None:
    """Run the scheduler with the current configuration."""
    config = get_json_config(ctx)
    check_valid_config(config)
    set_scheduler_options(config)
    click.echo("Running scheduler, please give it up to a minute...")
    schedule_list = run_using_config(config.combined_config)
    schedule_handler = ScheduleHandler()
    schedule_handler.load_schedules(schedule_list)
    ctx.obj[HANDLER_KEY] = schedule_handler
    show_schedule_viewer(ctx)
    handle_schedule_saving(schedule_list)

def set_scheduler_options(config: JsonConfig) -> None:
    """Set scheduler options interactively."""
    if click.confirm("Do you want to overwrite the config optimizations?", default=False):
        config.set_optimization(select_optimizations())
    config.set_limit(click.prompt("Enter the maximum number of schedules to generate", type=click.IntRange(min=1, max=100), default=1))

def select_optimizations() -> list[OptimizerFlags]:
    """Prompt the user to select optimization flags."""
    optimizations = [
        OptimizerFlags.FACULTY_COURSE,
        OptimizerFlags.FACULTY_ROOM,
        OptimizerFlags.FACULTY_LAB,
        OptimizerFlags.SAME_ROOM,
        OptimizerFlags.SAME_LAB,
        OptimizerFlags.PACK_ROOMS,
    ]
    selected = [flag for flag in optimizations if click.confirm(f"Optimize by {flag}?", default=True)]
    return selected

def show_schedule_viewer(ctx: click.Context) -> None:
    """Show the schedule viewer."""
    from .schedule_viewer import schedule_viewer
    cli.add_command(schedule_viewer)
    try:
        schedule_viewer.main(standalone_mode=False, obj=ctx.obj)
    except SystemExit:
        pass

def handle_schedule_saving(schedule_list: list[list[CourseInstanceJSON]]) -> None:
    """Handle saving the generated schedules."""
    typing = click.prompt(
        "\nDo you want to save the schedule(s) as a Json, CSV, both or none?",
        type=click.Choice(['json', 'csv', 'both', 'none']),
        default="csv"
    )
    if typing == 'none':
        click.echo("Not saving the file.")
        click.echo("Run complete.")
        return
    name = click.prompt("Enter the filename (without extension)", default="schedules")
    if typing in ('json', 'both'):
        try:
            write_as_json(schedule_list, name)
            click.echo(f"Schedules saved as {name}.json")
        except Exception as e:
            click.echo(f"An error occurred while writing JSON: {e}")
    if typing in ('csv', 'both'):
        try:
            write_as_csv(schedule_list, name)
            click.echo(f"Schedules saved as {name}.csv")
        except Exception as e:
            click.echo(f"An error occurred while writing CSV: {e}")
    click.echo("Run complete.")