import click
from click_shell import shell
from scheduler.config import Meeting

from .base_cli import clear, get_json_config, run, save, undo, redo
from ..model.time_slot import TimeSlot

DAY_TO_INDEX = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5}
INDEX_TO_DAY = {1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI"}


# ===== Time Slot Shell =====
@shell(
    prompt="time slot> ",
    intro="You may now add, modify, or delete time blocks and class patterns.\nYou may also set the maximum time gap and minimum time overlap.\nType 'help' to see available commands, 'exit' to return to main shell.\n",
)
def time_slot() -> None:
    """Manage time slots"""
    time_slot.add_command(show_time_slot)
    time_slot.add_command(clear)
    time_slot.add_command(run)
    time_slot.add_command(save)
    time_slot.add_command(undo)
    time_slot.add_command(redo)


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
        start_time = click.prompt("Meeting start time (e.g., 9 or 09:00)", default="")
        if start_time == "":
            start_time = None
        else:
            start_time = normalize_time(start_time)

        duration = click.prompt("Duration (minutes)", type=click.IntRange(min=0))
        lab = click.confirm("Is this a lab meeting?", default=False)
        if start_time == "":
            start_time = None
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
    cp_start_time = click.prompt(
        "Class pattern start time (e.g., 9 or 09:00)", default=""
    )
    if cp_start_time == "":
        cp_start_time = None
    else:
        cp_start_time = normalize_time(cp_start_time)
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
    click.echo(json_config.time_block_str())
    index = click.prompt(
        "Enter the number time block to delete",
        type=click.IntRange(
            0, len(json_config.time_slot_config.times.get(day, [])) - 1
        ),
    )
    try:
        click.echo(
            TimeSlot.del_time_block(
                json_config=json_config, day_index=day_index, index=index
            )
        )
    except ValueError as e:
        click.echo(e)
        return
    while click.confirm("Delete another time block?", default=False):
        click.echo(json_config.time_block_str())
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
    click.echo(json_config.class_pattern_str())
    index = click.prompt(
        "Enter the number class pattern to delete",
        type=click.IntRange(0, len(json_config.time_slot_config.classes) - 1),
    )
    try:
        click.echo(TimeSlot.del_class_pattern(json_config=json_config, index=index))
    except ValueError as e:
        click.echo(e)
        return
    while click.confirm("Delete another class pattern?", default=False):
        click.echo(json_config.class_pattern_str())
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
    click.echo(json_config.time_block_str())
    index = click.prompt(
        "Enter the number time block to modify",
        type=click.IntRange(
            0, len(json_config.time_slot_config.times.get(day, [])) - 1
        ),
    )
    old_time_block = json_config.time_slot_config.times.get(day, [])[index]
    start = normalize_time(
        click.prompt("Start time (e.g., 9 or 09:00)", default=old_time_block.start)
    )
    end = normalize_time(
        click.prompt("End time (e.g., 9 or 09:00)", default=old_time_block.end)
    )
    spacing = click.prompt(
        "Spacing (minutes)", type=click.IntRange(min=0), default=old_time_block.spacing
    )
    click.echo(
        TimeSlot.mod_time_block(
            json_config=json_config,
            day_index=day_index,
            index=index,
            start=start if start is not None else old_time_block.start,
            end=end if end is not None else old_time_block.end,
            spacing=spacing if spacing is not None else old_time_block.spacing,
        )
    )


@time_slot.command()
@click.pass_context
def modify_class_pattern(ctx: click.Context) -> None:
    """Modify a class pattern."""
    json_config = get_json_config(ctx)
    click.echo(json_config.class_pattern_str())
    index = click.prompt(
        "Enter the number class pattern to modify",
        type=click.IntRange(0, len(json_config.time_slot_config.classes) - 1),
    )
    old_class_pattern = json_config.time_slot_config.classes[index]
    creds = click.prompt(
        "Credits", type=click.IntRange(min=1), default=old_class_pattern.credits
    )
    meetings: list[Meeting] = old_class_pattern.meetings

    def add_meeting() -> None:
        meeting_day = click.prompt(
            "Meeting day",
            type=click.Choice(DAYS, case_sensitive=False),
            default=old_class_pattern.day,
        ).upper()
        start_time = normalize_time(
            click.prompt("Meeting start time (e.g., 9 or 09:00)", default=None)
        )
        duration = click.prompt("Duration (minutes)", type=click.IntRange(min=0))
        lab = click.confirm("Is this a lab meeting?", default=False)
        meeting = Meeting(
            day=meeting_day, start_time=start_time, duration=duration, lab=lab
        )
        meetings.append(meeting)

    if click.confirm(
        "Modify meetings? (You will have to create a list of meetings from scratch)",
        default=False,
    ):
        meetings = []
        add_meeting()
        while click.confirm("Add another meeting?", default=False):
            add_meeting()
    disabled = click.confirm(
        "Do you want to disable this class pattern?", default=old_class_pattern.disabled
    )
    cp_start_time = normalize_time(
        click.prompt(
            "Class pattern start time (e.g., 9 or 09:00)",
            default=old_class_pattern.start_time,
        )
    )
    click.echo(
        TimeSlot.mod_class_pattern(
            json_config=json_config,
            index=index,
            creds=creds if creds is not None else old_class_pattern.creits,
            meetings=meetings if meetings is not None else old_class_pattern.meetings,
            disabled=disabled if disabled is not None else old_class_pattern.disabled,
            start_time=cp_start_time
            if cp_start_time is not None
            else old_class_pattern.start_time,
        )
    )


@time_slot.command()
@click.pass_context
def set_max_time_gap(ctx: click.Context) -> None:
    """Set max time gap."""
    json_config = get_json_config(ctx)
    max_time_gap = click.prompt("Max time gap (minutes)", type=click.IntRange(min=0))
    click.echo(
        TimeSlot.set_max_time_gap(json_config=json_config, max_time_gap=max_time_gap)
    )


@time_slot.command()
@click.pass_context
def set_min_time_overlap(ctx: click.Context) -> None:
    """Set min time overlap."""
    json_config = get_json_config(ctx)
    min_time_overlap = click.prompt(
        "Min time overlap (minutes)", type=click.IntRange(min=0)
    )
    click.echo(
        TimeSlot.set_min_time_overlap(
            json_config=json_config, min_time_overlap=min_time_overlap
        )
    )


@time_slot.command(name="show")
@click.pass_context
def show_time_slot(ctx: click.Context) -> None:
    """Show time slot configuration when in the time slot sub-shell"""
    config = get_json_config(ctx)
    click.echo(config.time_slot_str())
