import click
from enum import Enum
from click_shell import shell
from .base_cli import clear, HANDLER_KEY
from ..model import ScheduleHandler

class DisplayMode(Enum):
    """ Modes for displaying schedules. """
    DEFAULT = "default"
    FACULTY = "faculty"
    ROOM = "room"

def navigate_schedules(schedule_handler: ScheduleHandler, mode: DisplayMode) -> None:
    """Navigate through schedules interactively."""
    schedules = schedule_handler.schedules
    idx = 0
    while 0 <= idx < len(schedules):
        quit_loop = False
        match mode:
            case DisplayMode.ROOM:
                click.echo (f"Schedule {idx + 1}:\n{ScheduleHandler.room_schedule(schedules[idx])}")
            case DisplayMode.FACULTY:
                click.echo (f"Schedule {idx + 1}:\n{ScheduleHandler.faculty_schedule(schedules[idx])}")
            case _:
                click.echo (f"Schedule {idx + 1}:\n{ScheduleHandler.format_schedule(schedules[idx])}")
        while True:
            user_input = click.prompt("Type 'n' for next, 'p' for previous, 'q' to quit", default='n',
                                      type=click.Choice(['n', 'p', 'q']), show_choices=False).lower()
            match user_input:
                case 'n':
                    if idx < len(schedules) - 1:
                        idx += 1
                        break
                    else:
                        click.echo("Already at the last schedule.")
                case 'p':
                    if idx > 0:
                        idx -= 1
                        break
                    else:
                        click.echo("Already at the first schedule.")
                case _:
                    quit_loop = True
                    break
        if quit_loop: break

def get_schedule_handler(ctx: click.Context) -> ScheduleHandler:
    """Retrieve the ScheduleHandler from the context."""
    schedule_handler: ScheduleHandler = ctx.obj.get(HANDLER_KEY)
    if not schedule_handler:
        raise click.ClickException("No schedules loaded. Please do 'load_schedules <file_path>' first.")
    return schedule_handler

@shell(prompt="schedule-viewer> ", intro="You may now view the schedules.\n Type 'help' to see available commands, 'quit' to exit.\n") # type: ignore
@click.pass_context
def schedule_viewer(ctx: click.Context) -> None:
    """Manage rooms."""
    ctx.ensure_object(dict)
    schedule_viewer.add_command(clear)

@schedule_viewer.command() # type: ignore
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show schedules in default mode."""
    schedule_handler = get_schedule_handler(ctx)
    navigate_schedules(schedule_handler, DisplayMode.DEFAULT)

@schedule_viewer.command() # type: ignore
@click.pass_context
def show_rooms(ctx: click.Context) -> None:
    """Show schedules by room."""
    schedule_handler = get_schedule_handler(ctx)
    navigate_schedules(schedule_handler, DisplayMode.ROOM)

@schedule_viewer.command() # type: ignore
@click.pass_context
def show_faculty(ctx: click.Context) -> None:
    """Show schedules by faculty."""
    schedule_handler = get_schedule_handler(ctx)
    navigate_schedules(schedule_handler, DisplayMode.FACULTY)