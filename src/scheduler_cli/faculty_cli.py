import click
from click_shell import shell
from scheduler import FacultyConfig
from .base_cli import get_json_config, show
from .json import JsonConfig

"""
This module implements a command-line interface (CLI) for managing faculty in the configuration file.
It allows users to add, modify and delete faculty.

The ctx.obj dictionary is used to store the current configuration state across different commands.
To utilize it for a command:

1- Ensure @click.pass_context is above the command function definition.
2- Add a parameter ctx: click.Context to the command function.
3- If you want to add something to the context object, use ctx.obj[key] = value.

To read up on how to use click, visit: https://click.palletsprojects.com/en/stable/
"""

# ===== Faculty shell =====
@shell(prompt="faculty> ", intro="You may now add, modify, or delete faculty.\nType 'help' to see available commands, 'exit' to return to main shell.\n") # type: ignore
def faculty() -> None:
    """Manage faculty"""
    faculty.add_command(show)

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
        day = click.prompt("Day name", type=click.Choice(["MON", "TUE", "WED", "THU", "FRI"], case_sensitive=False), show_choices=True).upper()
        time_ranges_input = click.prompt("Time ranges for this day (e.g., 9-11, 13-15 or 09:00-11:00)")
        time_ranges = [normalize_range(r) for r in time_ranges_input.split(',') if r.strip()]
        times.setdefault(day, []).extend(time_ranges)
    return times

def add_course_preferences(json_config: JsonConfig, default: bool) -> dict[str, int]:
    """Helper function to add course preferences for a faculty member."""
    course_preferences = {}
    course_ids = [c.course_id for c in json_config.scheduler_config.courses]
    while click.confirm("Add course preference?", default=default):
        course = click.prompt("Course ID", type=click.Choice(course_ids), show_choices=False)
        preference = click.prompt("Preference score", type=click.Choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), show_choices=True)
        course_preferences[course] = preference
    return course_preferences

def add_room_preferences(json_config: JsonConfig, default: bool) -> dict[str, int]:
    """Helper function to add room preferences for a faculty member."""
    room_preferences = {}
    room_ids = [room for room in json_config.scheduler_config.rooms]
    while click.confirm("Add room preference?", default=default):
        room = click.prompt("Room ID", type=click.Choice(room_ids), show_choices=False)
        preference = click.prompt("Preference score", type=click.Choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), show_choices=True)
        room_preferences[room] = preference
    return room_preferences

def add_lab_preferences(json_config: JsonConfig, default: bool) -> dict[str, int]:
    """Helper function to add lab preferences for a faculty member."""
    lab_preferences = {}
    lab_ids = [lab for lab in json_config.scheduler_config.labs]
    while click.confirm("Add lab preference?", default=default):
        lab = click.prompt("Lab ID", type=click.Choice(lab_ids), show_choices=False)
        preference = click.prompt("Preference score", type=click.Choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), show_choices=True)
        lab_preferences[lab] = preference
    return lab_preferences

@faculty.command() # type: ignore
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a new faculty member."""
    json_config = get_json_config(ctx)
    name = click.prompt("Faculty member's name")
    maximum_credits = click.prompt("Maximum credit hours", type=int)
    minimum_credits = click.prompt("Minimum credit hours", type=int)
    unique_course_limit = click.prompt("Unique course limit", type=int)
    times = add_times(False)
    course_preferences = add_course_preferences(json_config, False)
    room_preferences = add_room_preferences(json_config, False)
    lab_preferences = add_lab_preferences(json_config, False)
    faculty_config = FacultyConfig(name = name, maximum_credits = maximum_credits, minimum_credits = minimum_credits,
                                  unique_course_limit = unique_course_limit, times = times, course_preferences = course_preferences,
                                  room_preferences=room_preferences, lab_preferences=lab_preferences)
    json_config.scheduler_config.faculty.append(faculty_config)
    click.echo(f"Faculty '{name}' added.")

@faculty.command()  # type: ignore
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete a faculty member."""
    faculty_list = get_json_config(ctx).scheduler_config.faculty
    name = click.prompt("Enter the name of the faculty to delete")
    faculty_obj = next((f for f in faculty_list if f.name == name), None)
    if not faculty_obj:
        click.echo(f"Faculty '{name}' not found.")
        return
    faculty_list.remove(faculty_obj)
    click.echo(f"Faculty '{name}' deleted.")

@faculty.command() # type: ignore
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify an existing faculty member."""
    json_config = get_json_config(ctx)
    faculty_list = json_config.scheduler_config.faculty
    name = click.prompt("Enter the name of the faculty to modify")
    faculty_obj = next((f for f in faculty_list if f.name == name), None)
    if not faculty_obj:
        click.echo(f"Faculty '{name}' not found.")
        return
    new_name = click.prompt("Faculty member's name", type=str, default=faculty_obj.name)
    maximum_credits = click.prompt("Maximum credit hours", type=int, default=faculty_obj.maximum_credits)
    minimum_credits = click.prompt("Minimum credit hours", type=int, default=faculty_obj.minimum_credits)
    unique_course_limit = click.prompt("Unique course limit", type=int, default=faculty_obj.unique_course_limit)
    times = faculty_obj.times
    if click.confirm("Modify available times?", default=False):
        times = add_times(True)
    course_preferences = faculty_obj.course_preferences.copy()
    if click.confirm("Modify course preferences? (you will create a new one from scratch)", default=False):
        course_preferences = add_course_preferences(json_config, True)
    room_preferences = faculty_obj.room_preferences.copy()
    if click.confirm("Modify room preferences? (you will create a new one from scratch)", default=False):
        room_preferences = add_room_preferences(json_config, True)
    lab_preferences = faculty_obj.lab_preferences.copy()
    if click.confirm("Modify lab preferences? (you will create a new one from scratch)", default=False):
        lab_preferences = add_lab_preferences(json_config, True)
    faculty_config = FacultyConfig(name=new_name, maximum_credits=maximum_credits, minimum_credits=minimum_credits,
                                   unique_course_limit=unique_course_limit, times=times,
                                   course_preferences=course_preferences,
                                   room_preferences=room_preferences, lab_preferences=lab_preferences)
    for i, f in enumerate(faculty_list):
        if f.name == name:
            faculty_list[i] = faculty_config
            break
    click.echo(f"Faculty '{name}' modified.")