import click
import types
from click_shell import shell
from scheduler import FacultyConfig
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
NO_CONFIG_LOADED: str = "No configuration loaded. Please do 'load <config.json>' first."

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

def get_json_config(ctx: click.Context) -> JsonConfig:
    """Helper function to get the current JSON configuration."""
    config: JsonConfig = ctx.obj.get(CONFIG_KEY)
    if not config:
        raise click.ClickException(NO_CONFIG_LOADED)
    return config

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

# ===== Faculty shell =====
@shell(prompt="faculty> ", intro="You may now add, modify, or delete faculty.\nType 'help' to see available commands, 'exit' to return to main shell.\n") # type: ignore
@click.pass_context
def faculty(ctx: click.Context) -> None:
    """Manage faculty"""
    config = ctx.obj.get(CONFIG_KEY)
    if not config:
        click.echo(NO_CONFIG_LOADED)
        ctx.exit(1)
    faculty.add_command(show)
    faculty.add_command(save)

def normalize_range(r: str) -> str:
    """
    Normalize a time range to HH:MM-HH:MM format.
    This function is what allows users to enter times as 9-11 instead of 09:00-11:00
    """
    parts = r.strip().split('-')
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        return f"{int(parts[0]):02d}:00-{int(parts[1]):02d}:00"
    return r.strip()

def add_times(default: bool) -> dict[str, list[str]]:
    """Helper function to add available times for a faculty member."""
    times: dict[str, list[str]] = {}
    while click.confirm("Add available time for a day? (MON, TUE, WED, THU, FRI)", default=default):
        day = click.prompt("Day name").upper()
        time_ranges_input = click.prompt("Time ranges for this day (e.g., 9-11, 13-15 or 09:00-11:00)")
        time_ranges = [normalize_range(r) for r in time_ranges_input.split(',') if r.strip()]
        times.setdefault(day, []).extend(time_ranges)
    return times

def add_course_preferences(default: bool) -> dict[str, int]:
    """Helper function to add course preferences for a faculty member."""
    course_preferences = {}
    while click.confirm("Add course preference?", default=default):
        course = click.prompt("Course ID")
        preference = click.prompt("Preference score", type=int)
        course_preferences[course] = preference
    return course_preferences

def add_room_preferences(default: bool) -> dict[str, int]:
    """Helper function to add room preferences for a faculty member."""
    room_preferences = {}
    while click.confirm("Add room preference?", default=default):
        room = click.prompt("Room ID")
        preference = click.prompt("Preference score", type=int)
        room_preferences[room] = preference
    return room_preferences

def add_lab_preferences(default: bool) -> dict[str, int]:
    """Helper function to add lab preferences for a faculty member."""
    lab_preferences = {}
    while click.confirm("Add lab preference?", default=default):
        lab = click.prompt("Lab ID")
        preference = click.prompt("Preference score", type=int)
        lab_preferences[lab] = preference
    return lab_preferences

@faculty.command() # type: ignore
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a new faculty member."""
    name = click.prompt("Faculty member's name")
    maximum_credits = click.prompt("Maximum credit hours", type=int)
    minimum_credits = click.prompt("Minimum credit hours", type=int)
    unique_course_limit = click.prompt("Unique course limit", type=int)
    times = add_times(False)
    course_preferences = add_course_preferences(False)
    room_preferences = add_room_preferences(False)
    lab_preferences = add_lab_preferences(False)
    faculty_config = FacultyConfig(name = name, maximum_credits = maximum_credits, minimum_credits = minimum_credits,
                                  unique_course_limit = unique_course_limit, times = times, course_preferences = course_preferences,
                                  room_preferences=room_preferences, lab_preferences=lab_preferences)
    get_json_config(ctx).scheduler_config.faculty.append(faculty_config)
    click.echo(f"Faculty '{name}' added.")

@faculty.command() # type: ignore
@click.argument("name")
def delete(name: str) -> None:
    click.echo(f"Faculty '{name}' deleted.")

@faculty.command() # type: ignore
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify an existing faculty member."""
    faculty_list = get_json_config(ctx).scheduler_config.faculty
    name = click.prompt("Enter the name of the faculty to modify")
    faculty_obj = next((f for f in faculty_list if f.name == name), None)
    if not faculty_obj:
        click.echo(f"Faculty '{name}' not found.")
        return
    new_name = click.prompt("Faculty member's name", type=str, default=faculty_obj.name)
    maximum_credits = click.prompt("Maximum credit hours", type=int, default=faculty_obj.maximum_credits)
    minimum_credits = click.prompt("Minimum credit hours", type=int, default=faculty_obj.minimum_credits)
    unique_course_limit = click.prompt("Unique course limit", type=int, default=faculty_obj.unique_course_limit)
    times = faculty_obj.times.copy()
    if click.confirm("Modify available times?", default=False):
        times = add_times(True)
    course_preferences = faculty_obj.course_preferences.copy()
    if click.confirm("Modify course preferences? (you will create a new one from scratch)", default=False):
        course_preferences = add_course_preferences(True)
    room_preferences = faculty_obj.room_preferences.copy()
    if click.confirm("Modify room preferences? (you will create a new one from scratch)", default=False):
        room_preferences = add_room_preferences(True)
    lab_preferences = faculty_obj.lab_preferences.copy()
    if click.confirm("Modify lab preferences? (you will create a new one from scratch)", default=False):
        lab_preferences = add_lab_preferences(True)
    click.echo(f"Faculty '{new_name}' modified.")