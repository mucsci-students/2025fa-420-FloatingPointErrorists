import click
from click_shell import shell
from scheduler.config import Meeting

from .base_cli import clear, get_json_config, run, save
from ..model.time_slot import TimeSlot

DAY_TO_INDEX = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5}
INDEX_TO_DAY = {1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI"}


# ===== Time Slot Shell =====
@shell(
    prompt="time slot>",
    intro="You may now add, modify, or delete time blocks and class patterns. \nType 'help' to see available commands, 'exit' to return to main shell.\n",
)
def time_slot() -> None:
    """Manage time slots"""
    time_slot.add_command(show_time_slot)
    time_slot.add_command(clear)
    time_slot.add_command(run)
    time_slot.add_command(save)


def normalize_time(time: str) -> str:
    """
    Normalize a time to HH:MM format.
    This function is what allows users to enter times as 9 instead of 09:00
    """
    time = time.strip()
    if ":" in time:
        hour, minute = time.split(":")
        hour = int(hour)
        minute = int(minute)
    else:
        hour, minute = int(time), 0
    return f"{hour:02d}:{minute:02d}"


DAYS = ["MON", "TUE", "WED", "THU", "FRI"]


@time_slot.command()
@click.pass_context
def add_time_block(ctx: click.Context) -> None:
    """Add a time block"""
    json_config = get_json_config(ctx)
    day = click.prompt(
        "Enter a day",
        type=click.Choice(DAYS, case_sensitive=False),
        show_choices=True,
    ).upper()
    day_index = DAY_TO_INDEX[day]
    start = normalize_time(click.prompt("Start time (e.g., 9 or 09:00)"))
    end = normalize_time(click.prompt("End time (e.g., 9 or 09:00)"))
    spacing = click.prompt("Spacing (minutes)", type=click.IntRange(min=0))
    click.echo(TimeSlot.add_time_block(json_config, day_index, start, spacing, end))


@time_slot.command()
@click.pass_context
def add_class_pattern(ctx: click.Context) -> None:
    """Add a class pattern"""
    json_config = get_json_config(ctx)
    creds = click.prompt("Credits", type=int)
    meetings: list[Meeting] = []

    def add_meeting() -> None:
        meeting_day = click.prompt(
            "Meeting day", type=click.Choice(DAYS, case_sensitive=False)
        )
        start_time = normalize_time(click.prompt("Start time (e.g., 9 or 09:00)"))
        duration = click.prompt("Duration (minutes)", type=click.IntRange(min=0))
        lab = click.confirm("Is this a lab meeting?", default=False)
        meeting = Meeting(
            day=meeting_day, start_time=start_time, duration=duration, lab=lab
        )
        meetings.append(meeting)

    add_meeting()
    disabled = click.confirm(
        "Do you want to disable this class pattern?", default=False
    )
    while click.confirm("Add another meeting?", default=False):
        add_meeting()
    cp_start_time = normalize_time(click.prompt("Start time (e.g., 9 or 09:00)"))
    click.echo(
        TimeSlot.add_class_pattern(
            json_config=json_config,
            creds=creds,
            meetings=meetings,
            disabled=disabled,
            start_time=cp_start_time,
        )
    )


@time_slot.command()
@click.pass_context
def delete_time_block(ctx: click.Context) -> None:
    """Delete a time block."""
    json_config = get_json_config(ctx)
    day = click.prompt(
        "Enter the day to delete from", type=click.Choice(DAYS, case_sensitive=False)
    ).upper()
    day_index = DAY_TO_INDEX[day]
    if len(json_config.time_slot_config.times.get(day, [])) == 0:
        click.echo("No time blocks to delete.")
        return
    click.echo(json_config.time_slot_str())
    index = click.prompt(
        "Enter the number time block to delete",
        type=click.IntRange(
            0, len(json_config.time_slot_config.times.get(day, [])) - 1
        ),
    )
    click.echo(
        TimeSlot.del_time_block(
            json_config=json_config, day_index=day_index, index=index
        )
    )
    while click.confirm("Delete another time block?", default=False):
        click.echo(json_config.time_slot_str())
        index = click.prompt(
            "Enter the number time block to delete",
            type=click.IntRange(
                0, len(json_config.time_slot_config.times.get(day, [])) - 1
            ),
        )
        click.echo(
            TimeSlot.del_time_block(
                json_config=json_config, day_index=day_index, index=index
            )
        )


@time_slot.command()
@click.pass_context
def delete_class_pattern(ctx: click.Context) -> None:
    """Delete a class pattern."""
    json_config = get_json_config(ctx)
    index = click.prompt(
        "Enter the number class pattern to delete",
        type=click.IntRange(0, len(json_config.time_slot_config.classes) - 1),
    )
    click.echo(TimeSlot.del_class_pattern(json_config=json_config, index=index))
    while click.confirm("Delete another class pattern?", default=False):
        click.echo(json_config.time_slot_str())
        index = click.prompt(
            "Enter the number class pattern to delete",
            type=click.IntRange(0, len(json_config.time_slot_config.classes) - 1),
        )
        click.echo(TimeSlot.del_class_pattern(json_config=json_config, index=index))


@time_slot.command()
@click.pass_context
def modify_time_block(ctx: click.Context) -> None:
    """Modify a time block."""
    json_config = get_json_config(ctx)
    day = click.prompt(
        "Enter the day to modify from", type=click.Choice(DAYS, case_sensitive=False)
    )
    day_index = DAY_TO_INDEX[day]
    if len(json_config.time_slot_config.times.get(day, [])) == 0:
        click.echo("No time blocks to modify.")
        return
    click.echo(json_config.time_slot_str())
    index = click.prompt(
        "Enter the number time block to modify",
        type=click.IntRange(
            0, len(json_config.time_slot_config.times.get(day, [])) - 1
        ),
    )
    json_config.time_slot_config.times.get(day, [])[index]
    start = normalize_time(click.prompt("Start time (e.g., 9 or 09:00)"))
    end = normalize_time(click.prompt("End time (e.g., 9 or 09:00)"))
    spacing = click.prompt("Spacing (minutes)", type=click.IntRange(min=0))
    click.echo(
        TimeSlot.mod_time_block(
            day_index=day_index,
            index=index,
            json_config=json_config,
            start=start,
            end=end,
            spacing=spacing,
        )
    )


@time_slot.command()
@click.pass_context
def modify_class_pattern(ctx: click.Context) -> None:
    """Modify a class pattern."""
    json_config = get_json_config(ctx)
    index = click.prompt(
        "Enter the number class pattern to modify",
        type=click.IntRange(0, len(json_config.time_slot_config.classes) - 1),
    )
    json_config.time_slot_config.classes[index]
    creds = click.prompt("Credits", type=int)
    meetings: list[Meeting] = []

    def add_meeting() -> None:
        meeting_day = click.prompt(
            "Meeting day", type=click.Choice(DAYS, case_sensitive=False)
        ).upper()
        start_time = normalize_time(click.prompt("Start time (e.g., 9 or 09:00)"))
        duration = click.prompt("Duration (minutes)", type=click.IntRange(min=0))
        lab = click.confirm("Is this a lab meeting?", default=False)
        meeting = Meeting(
            day=meeting_day, start_time=start_time, duration=duration, lab=lab
        )
        meetings.append(meeting)

    add_meeting()
    while click.confirm("Add another meeting?", default=False):
        add_meeting()
    disabled = click.confirm(
        "Do you want to disable this class pattern?", default=False
    )
    cp_start_time = normalize_time(click.prompt("Start time (e.g., 9 or 09:00)"))
    click.echo(
        TimeSlot.mod_class_pattern(
            index=index,
            json_config=json_config,
            creds=creds,
            meetings=meetings,
            disabled=disabled,
            start_time=cp_start_time,
        )
    )


@time_slot.command(name="show")
@click.pass_context
def show_time_slot(ctx: click.Context) -> None:
    """Show time slot configuration when in the time slot sub-shell"""
    config = get_json_config(ctx)
    click.echo(config.time_slot_str())
