import click
from click_shell import shell
from .base_cli import get_json_config, show

"""
This module implements a command-line interface (CLI) for managing courses in the configuration file.
It allows users to add, modify and delete courses.

The ctx.obj dictionary is used to store the current configuration state across different commands.
To utilize it for a command:

1- Ensure @click.pass_context is above the command function definition.
2- Add a parameter ctx: click.Context to the command function.
3- If you want to add something to the context object, use ctx.obj[key] = value.

To read up on how to use click, visit: https://click.palletsprojects.com/en/stable/
"""

# ===== Course Shell =====
@shell(prompt="courses> ", intro="You may now add, modify, or delete courses.\nType 'help' to see available commands, 'quit' to exit.\n") # type: ignore
def courses() -> None:
    """Manage courses."""
    courses.add_command(show)

@courses.command() # type: ignore
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a course."""
    json_config = get_json_config(ctx)
    room_ids = [room for room in json_config.scheduler_config.rooms]
    lab_ids = [lab for lab in json_config.scheduler_config.labs]
    course_ids = [c.course_id for c in json_config.scheduler_config.courses]
    faculty_names = [faculty.name for faculty in json_config.scheduler_config.faculty]
    ID = click.prompt("Enter course ID", type=str)
    course_credits = click.prompt("Enter course credits", type=int)
    room = []
    while click.confirm("Add room(s)?", default=False):
        room.append(click.prompt("Enter room name", type=click.Choice(room_ids), show_default=False))
    lab = []
    while click.confirm("Add lab(s)?", default=False):
        lab.append(click.prompt("Enter lab name", type=click.Choice(lab_ids), show_default=False))
    conflicts = []
    while click.confirm("Add conflict(s)?", default=False):
        conflicts.append(click.prompt("Enter course conflict", type=click.Choice(course_ids), show_default=False))
    faculty = []
    while click.confirm("Add faculty?", default=False):
        faculty.append(click.prompt("Enter faculty name", type=click.Choice(faculty_names), show_default=False))
    courses.add_course(json_config, ID, course_credits, room, lab, conflicts, faculty)

@courses.command()
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete a course."""
    json_config = get_json_config(ctx)
    courses.print(json_config)
    crs = click.prompt("Enter the number course to delete", type=int)
    courses.delete_course(json_config, crs)
    click.echo(f"course number {crs} deleted")
    while click.confirm("Delete another?", default=False):
        crs = click.prompt("Enter the number course to delete", type=int)
        courses.delete_course(json_config, crs)
        click.echo(f"course number {crs} deleted")


@courses.command()
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify a course."""
    json_config = get_json_config(ctx)
    courses.print(json_config)
    index = click.prompt("Enter the number course to modify", type=int)
    old_course = json_config.scheduler_config.courses[index]
    room_ids = [room for room in json_config.scheduler_config.rooms]
    lab_ids = [lab for lab in json_config.scheduler_config.labs]
    course_ids = [c.course_id for c in json_config.scheduler_config.courses]
    faculty_names = [faculty.name for faculty in json_config.scheduler_config.faculty]
    ID = click.prompt("Enter course ID", type=str, default=old_course.course_id)
    course_credits = click.prompt("Enter course credits", type=int, default=old_course.course_credits)
    room = []
    while click.confirm("Modify room(s)?", default=False):
        room.append(click.prompt("Enter room name", type=click.Choice(room_ids), show_default=False))
    lab = []
    while click.confirm("Modify lab(s)?", default=False):
        lab.append(click.prompt("Enter lab name", type=click.Choice(lab_ids), show_default=False))
    conflicts = []
    while click.confirm("Modify conflict(s)?", default=False):
        conflicts.append(click.prompt("Enter course conflict", type=click.Choice(course_ids), show_default=False))
    faculty = []
    while click.confirm("Modify faculty?", default=False):
        faculty.append(click.prompt("Enter faculty name", type=click.Choice(faculty_names), show_default=False))
    courses.mod_course(index, ID, course_credits, room, lab, conflicts, faculty)