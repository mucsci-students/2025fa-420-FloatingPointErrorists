import time
from enum import Enum
import click
from click_shell import shell
from scheduler.json_types import CourseInstanceJSON

from ..model import ScheduleHandler, PdfWriter, PdfMode
from .base_cli import HANDLER_KEY, clear


class DisplayMode(Enum):
    """Modes for displaying schedules."""

    DEFAULT = "default"
    FACULTY = "faculty"
    ROOM = "room"

def pdf_export(mode: PdfMode, schedule: list[CourseInstanceJSON]) -> None:
    """Export the current schedule to a PDF file."""
    name = click.prompt("Enter filename for PDF export", default="schedule")
    PdfWriter.export_graph_pdf(
        ScheduleHandler.room_schedule_columns(schedule)
        if mode == PdfMode.ROOM
        else ScheduleHandler.faculty_schedule_columns(schedule),
        name,
        mode
    )
    click.echo(f"Schedule exported to {name}.pdf")
    time.sleep(1.5)

def navigate_schedules(schedule_handler: ScheduleHandler, mode: DisplayMode) -> None:
    """Navigate through schedules interactively."""
    schedules = schedule_handler.schedules
    idx = 0
    while True:
        match mode:
            case DisplayMode.ROOM:
                click.echo(
                    f"Schedule {idx + 1}:\n{ScheduleHandler.room_schedule_str(schedules[idx])}"
                )
            case DisplayMode.FACULTY:
                click.echo(
                    f"Schedule {idx + 1}:\n{ScheduleHandler.faculty_schedule_str(schedules[idx])}"
                )
            case _:
                click.echo(
                    f"Schedule {idx + 1}:\n{ScheduleHandler.format_schedule_str(schedules[idx])}"
                )
        user_input = click.prompt(
            "Type 'n' for next, 'p' for previous, 'q' to quit, 'e' to export to PDF",
            default="n",
            type=click.Choice(["n", "p", "q", "e"]),
            show_choices=False,
        ).lower()
        match user_input:
            case "e":
                pdf_export(PdfMode.ROOM if mode == DisplayMode.ROOM else PdfMode.FACULTY, schedules[idx])
            case "n":
                if idx < len(schedules) - 1:
                    idx += 1
                else:
                    idx = 0
            case "p":
                if idx > 0:
                    idx -= 1
                else:
                    idx = len(schedules) - 1
            case _:
                break


def get_schedule_handler(ctx: click.Context) -> ScheduleHandler:
    """Retrieve the ScheduleHandler from the context."""
    schedule_handler: ScheduleHandler = ctx.obj.get(HANDLER_KEY)
    if not schedule_handler:
        raise click.ClickException(
            "No schedules loaded. Please do 'load_schedules <file_path>' first."
        )
    return schedule_handler


@shell(
    prompt="schedule-viewer> ",
    intro="You may now view the schedules.\n Type 'help' to see available commands, 'quit' to exit.\n",
)  # type: ignore
@click.pass_context
def view_schedules(ctx: click.Context) -> None:
    """Shell to view schedules."""
    ctx.ensure_object(dict)
    view_schedules.add_command(clear)


@view_schedules.command()  # type: ignore
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show schedules in a tabular format."""
    schedule_handler = get_schedule_handler(ctx)
    navigate_schedules(schedule_handler, DisplayMode.DEFAULT)


@view_schedules.command()  # type: ignore
@click.pass_context
def show_rooms(ctx: click.Context) -> None:
    """Show schedules by room."""
    schedule_handler = get_schedule_handler(ctx)
    navigate_schedules(schedule_handler, DisplayMode.ROOM)


@view_schedules.command()  # type: ignore
@click.pass_context
def show_faculty(ctx: click.Context) -> None:
    """Show schedules by faculty."""
    schedule_handler = get_schedule_handler(ctx)
    navigate_schedules(schedule_handler, DisplayMode.FACULTY)
