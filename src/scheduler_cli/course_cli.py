import click
from click_shell import shell
from .base_cli import get_json_config, show, clear, save, run
from .courses import Course
from .json import JsonConfig

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
    courses.add_command(clear)
    courses.add_command(run)
    courses.add_command(save)

def get_course_index(json_config: JsonConfig, prompt_text: str) -> int:
    """Helper function to get a valid course index from the user."""
    max_index = len(json_config.scheduler_config.courses) - 1
    while True:
        index: int = click.prompt(prompt_text, type=int)
        if 0 <= index <= max_index:
            return index
        click.echo(f"Invalid index. Please enter a number between 0 and {max_index}.")

def add_new_rooms(valid_rooms: list[str], default: bool) -> list[str]:
    """Helper function to add rooms to a course."""
    rooms = []
    while click.confirm("Add room(s)?", default=default):
        rooms.append(click.prompt("Enter room name", type=click.Choice(valid_rooms), show_choices=False, show_default=False))
    return rooms

def add_new_labs(valid_labs: list[str], default: bool) -> list[str]:
    """Helper function to add labs to a course."""
    labs = []
    while click.confirm("Add labs(s)?", default=default):
        labs.append(click.prompt("Enter lab name", type=click.Choice(valid_labs), show_choices=False, show_default=False))
    return labs

def add_new_conflicts(valid_courses: list[str], default: bool) -> list[str]:
    """Helper function to add course conflicts to a course."""
    conflicts = []
    while click.confirm("Add conflict(s)?", default=default):
        conflicts.append(click.prompt("Enter course conflict", type=click.Choice(valid_courses), show_choices=False, show_default=False))
    return conflicts

def add_new_faculty(valid_faculty: list[str], default: bool) -> list[str]:
    """Helper function to add faculty to a course."""
    faculty = []
    while click.confirm("Add faculty?", default=default):
        faculty.append(click.prompt("Enter faculty name", type=click.Choice(valid_faculty), show_choices=False, show_default=False))
    return faculty

@courses.command() # type: ignore
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a course."""
    json_config = get_json_config(ctx)
    room_ids = json_config.scheduler_config.rooms
    lab_ids = json_config.scheduler_config.labs
    course_ids = [c.course_id for c in json_config.scheduler_config.courses]
    faculty_names = [faculty.name for faculty in json_config.scheduler_config.faculty]
    course_id = click.prompt("Enter course ID", type=str)
    course_credits = click.prompt("Enter course credits", type=int)
    room = add_new_rooms(room_ids, False)
    lab = add_new_labs(lab_ids, False)
    conflicts = add_new_conflicts(course_ids, False)
    faculty = add_new_faculty(faculty_names, False)
    Course.add_course(json_config, course_id, course_credits, room, lab, conflicts, faculty)
    click.echo(f"{course_id} added.")

@courses.command()  # type: ignore
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete a course."""
    json_config = get_json_config(ctx)
    if len(json_config.scheduler_config.courses) == 0:
        click.echo("No courses to delete.")
        return
    click.echo(Course.courses_string(json_config))
    index = get_course_index(json_config, "Enter the number of the course to delete")
    Course.del_course(index, json_config)
    click.echo(f"course number {index} deleted")
    while click.confirm("Delete another?", default=False):
        click.echo(Course.courses_string(json_config))
        index = click.prompt("Enter the number course to delete", type=int)
        Course.del_course(index, json_config)
        click.echo(f"course number {index} deleted.")

@courses.command()  # type: ignore
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify a course."""
    json_config = get_json_config(ctx)
    click.echo(Course.courses_string(json_config))
    if len(json_config.scheduler_config.courses) == 0:
        click.echo("No courses to modify.")
        return
    index = get_course_index(json_config, "Enter the number of the course to modify")
    old_course = json_config.scheduler_config.courses[index]
    course_id = click.prompt("Enter course ID", type=str, default=old_course.course_id)
    course_credits = click.prompt("Enter course credits", type=int, default=old_course.credits)
    room = old_course.room
    lab = old_course.lab
    conflicts = old_course.conflicts
    faculty = old_course.faculty
    valid_faculty = [f.name for f in json_config.scheduler_config.faculty]
    valid_courses = [c.course_id for c in json_config.scheduler_config.courses]
    if click.confirm("Modify course rooms? (you will create a new set from scratch)", default=False):
        room = add_new_rooms(json_config.scheduler_config.rooms, True)
    if click.confirm("Modify course labs? (you will create a new set from scratch)", default=False):
        lab = add_new_labs(json_config.scheduler_config.labs, True)
    if click.confirm("Modify course conflicts? (you will create a new set from scratch)", default=False):
        conflicts = add_new_conflicts(valid_courses, True)
    if click.confirm("Modify course faculty? (you will create a new set from scratch)", default=False):
        faculty = add_new_faculty(valid_faculty, True)
    Course.mod_course(index, json_config, course_id, course_credits, room, lab, conflicts, faculty)
    click.echo(f"course number {index} modified.")