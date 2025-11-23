import logging
import os
import signal
import sys
import threading
import time
import types

import click
from click_shell import shell
from scheduler import OptimizerFlags, Scheduler, CombinedConfig
from scheduler.models import CourseInstance
from scheduler_config_editor.model.langchain_client import LangchainClient

from ..model.json_config import JsonConfig
from ..model.schedule_writer import ScheduleWriter
from ..model.schedule_handler import ScheduleHandler

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
@shell(
    prompt="scheduler> ",
    intro="Welcome to the Scheduler CLI!\nType 'help' to see available commands, 'quit' to exit.\n",
)  # type: ignore
@click.pass_context
def base_cli(ctx: click.Context) -> None:
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
        raise click.ClickException(
            "No configuration loaded. Please do 'load-config <configuration>' first."
        )
    return config


def enable_configuration_commands() -> None:
    """Add all the sub-shells to the cli."""
    from .course_cli import courses
    from .faculty_cli import faculty
    from .lab_cli import labs
    from .room_cli import rooms

    base_cli.add_command(faculty)  # Add faculty sub-shell
    base_cli.add_command(courses)  # Add courses sub-shell
    base_cli.add_command(rooms)  # Add rooms sub-shell
    base_cli.add_command(labs)  # Add labs sub-shell
    base_cli.add_command(chat)  # Add chat command
    base_cli.add_command(undo)  # Add undo command
    base_cli.add_command(redo)  # Add redo command


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


@base_cli.command()  # type: ignore
def clear() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


# ====== JSON Commands ======
@base_cli.command()  # type: ignore
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
        raise click.ClickException(f"Invalid JSON: {e}") from e
    except TypeError as e:
        raise click.ClickException("Invalid Configuration") from e


@base_cli.command()  # type: ignore
@click.pass_context
def show(ctx: click.Context) -> None:
    """Show the loaded configuration."""
    config = get_json_config(ctx)
    click.echo(config)


@base_cli.command()  # type: ignore
@click.pass_context
def save(ctx: click.Context) -> None:
    """Save the current configuration back to the file."""
    try:
        config = get_json_config(ctx)
        config.save()
        click.echo("Configuration saved.")
    except PermissionError as e:
        raise click.ClickException(f"Permission error: {e}") from e


@base_cli.command()  # type: ignore
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
        from .schedule_cli import view_schedules

        base_cli.add_command(view_schedules)
        view_schedules.main(standalone_mode=False, obj=ctx.obj)
    except FileNotFoundError as e:
        raise click.ClickException(f"{e}") from e
    except ValueError as e:
        raise click.ClickException(f"{e}") from e


@base_cli.command()  # type: ignore
@click.pass_context
def run(ctx: click.Context) -> None:
    """Run the scheduler with the current configuration."""
    config = get_json_config(ctx)
    check_valid_config(config)
    set_scheduler_options(config)
    schedule_list = run_using_config(config.combined_config)
    schedule_handler = ScheduleHandler()
    schedule_handler.load_schedules(schedule_list)
    ctx.obj[HANDLER_KEY] = schedule_handler
    show_schedule_viewer(ctx)
    handle_schedule_saving(schedule_list)


@click.command()
@click.pass_context
def chat(ctx: click.Context) -> None:
    """Chat with the AI agent Jarvis to help with scheduling tasks."""
    try:
        langchain_client = LangchainClient(get_json_config(ctx))
    except ValueError as e:
        raise click.ClickException(f"{e}") from e
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    while True:
        command = click.prompt("Enter a prompt")
        if command.lower() in ("exit", "quit"):
            click.echo("Exiting chat.")
            break
        stop_event = threading.Event()
        spinner_thread = threading.Thread(
            target=spinner, args=(stop_event, "Jarvis is thinking")
        )
        spinner_thread.start()
        try:
            response = langchain_client.send_query(command)
        finally:
            stop_event.set()
            spinner_thread.join()
        click.echo(response)


@click.command()
@click.pass_context
def undo(ctx: click.Context) -> None:
    """Undo the last change made to the configuration."""
    try:
        get_json_config(ctx).undo()
        click.echo("Undid successfully.")
    except IndexError:
        click.echo("Nothing to undo.")


@click.command()
@click.pass_context
def redo(ctx: click.Context) -> None:
    """Redo the last change that was undone."""
    try:
        get_json_config(ctx).redo()
        click.echo("Redid successfully.")
    except IndexError:
        click.echo("Nothing to redo.")


def spinner(stop_event: threading.Event) -> None:
def spinner(stop_event: threading.Event, text: str) -> None:
    """Display a spinner while waiting for a response."""
    spinner_chars = "|/-\\"
    i = 0
    while not stop_event.is_set():
        click.echo(f"\r{text}... {spinner_chars[i % len(spinner_chars)]}", nl=False)
        time.sleep(0.1)
        i += 1
        # This is how I got it to clear the line properly. If you have a better way, please change it.
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()


def set_scheduler_options(config: JsonConfig) -> None:
    """Set scheduler options interactively."""
    if click.confirm(
        "Do you want to overwrite the config optimizations?", default=False
    ):
        config.set_optimization(select_optimizations())
    config.set_limit(
        click.prompt(
            "Enter the maximum number of schedules to generate",
            type=click.IntRange(min=1),
            default=config.combined_config.limit,
        )
    )


def run_using_config(combined_config: CombinedConfig) -> list[list["CourseInstance"]]:
    scheduler = Scheduler(combined_config)
    schedule_list = []
    # Temporarily silence all logging
    logging.disable(logging.CRITICAL)
    try:
        with click.progressbar(
            scheduler.get_models(),
            label="Generating schedules...",
            length=combined_config.limit,
        ) as bar:
            for schedule in bar:
                schedule_list.append(schedule)
    finally:
        logging.disable(logging.NOTSET)
    return schedule_list


def select_optimizations() -> list[OptimizerFlags]:
    """Prompt the user to select optimization flags."""
    selected = [
        flag
        for flag in OptimizerFlags
        if click.confirm(f"Optimize by {flag}?", default=True)
    ]
    return selected


def show_schedule_viewer(ctx: click.Context) -> None:
    """Show the schedule viewer."""
    from .schedule_cli import view_schedules

    base_cli.add_command(view_schedules)
    try:
        view_schedules.main(standalone_mode=False, obj=ctx.obj)
    except SystemExit:
        pass


def handle_schedule_saving(schedule_list: list[list[CourseInstance]]) -> None:
    """Handle saving the generated schedules."""
    typing = click.prompt(
        "\nDo you want to save the schedule(s) as a Json, CSV, both or none?",
        type=click.Choice(["json", "csv", "both", "none"]),
        default="csv",
    )
    if typing == "none":
        click.echo("Not saving the file.")
        click.echo("Run complete.")
        return
    name = click.prompt("Enter the filename (without extension)", default="schedules")
    if typing in ("json", "both"):
        try:
            ScheduleWriter.write_as_json(schedule_list, name)
            click.echo(f"Schedules saved as {name}.json")
        except Exception as e:
            click.echo(f"An error occurred while writing JSON: {e}")
    if typing in ("csv", "both"):
        try:
            ScheduleWriter.write_as_csv(schedule_list, name)
            click.echo(f"Schedules saved as {name}.csv")
        except Exception as e:
            click.echo(f"An error occurred while writing CSV: {e}")
    click.echo("Run complete.")
