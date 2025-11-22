import click
from click_shell import shell

from ..model.time_slot import TimeSlot
from ..model.json import JsonConfig
from scheduler.config import TimeBlock, Meeting, ClassPattern
from .base_cli import clear, get_json_config, run, save, show


# ===== Time Slot Shell =====
@shell(
    prompt="time slot>",
    intro="You may now add, modify, or delete time slots. \nType 'help' to see available commands, 'exit' to return to main shell.\n"
)

def time_slot() -> None:
    """Manage time slots"""
    time_slot.add_command(show)
    time_slot.add_command(clear)
    time_slot.add_command(run)
    time_clot.add_command(save)

def normalize_range(r: str) -> str:
    """
    Normalize a time range to HH:MM-HH:MM format.
    This function is what allows users to enter times as 9-11 instead of 09:00-11:00
    """
    parts = r.strip().split("-")
    if len(parts) == 1 and all(p.isdigit() for p in parts):
        return f"{int(parts[0]):02d}:00"
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        return f"{int(parts[0]):02d}:00-{int(parts[1]):02d}:00"
    return r.strip()

def get_start_end (range: str) -> Tuple[str, str]:
    """
    Takes a normalized range in HH:MM-HH:MM format.
    Returns the start and end of the range as a tuple.
    """
    start, end = normalize_range(range).split("-")
    return start, end

DAYS = ["MON", "TUE", "WED", "THU", "FRI"]

def add_timeblock(default: bool) -> dict[str, list[TimeBlock]]:
    """Helper function for adding time blocks to a time slot"""
    time_blocks: dict[str, list[TimeBlock]] = {
        "MON": [],
        "TUE": [],
        "WED": [],
        "THU": [],
        "FRI": []
    }

    def add_day() -> None:
        day = click.prompt(
            "Add a day name",
            type=click.Choice(DAYS, case_sensitive=False),
            show_choices=True,
        ).upper()
        time_block_input = click.prompt(
            "Time block for this day (e.g., 9-11, 13-15 or 09:00-11:00)"
        )

        start, end = get_start_end(time_block_input)
        spacing = click.prompt("Spacing (minutes)", type=int, min=0)
        block = TimeBlock(start=start, end=end, spacing=spacing)
        time_blocks[day].append(block)

    add_day()
    while click.confirm("Add another time block?", default=default):
        add_day()
    return time_blocks

def add_class_pattern(default: bool) -> dict[str, list[ClassPattern]]:
    """Helper function for adding class patterns to a time slot"""
    classes: list[ClassPattern] = []

    def add_class() -> None:
        credits = click.prompt("Credits", type=int)
        meetings: list[Meeting] = []

        def add_meeting() -> None:
            meeting_day = click.prompt("Meeting day", type=click.Choice(DAYS))
            start_time = normalize_range(click.prompt("Start time"))
            duration = click.prompt("Duration (minutes)", type=int, min=0)
            lab = click.confirm("Is this a lab meeting?", default=default)
            meeting = Meeting(day=meeting_day, start_time=start_time, duration=duration, lab=lab)
            meetings.append(meeting)

        add_meeting()
        disabled = click.confirm("Do you want to disable this class pattern?", default=False)
        while click.confirm("Add another meeting?", default=default):
            add_meeting()
        class_pattern = ClassPattern(credits=credits, meetings=meetings, disabled=disabled, start_time=start_time)
        classes.append(class_pattern)

    add_class()
    while click.confirm("Add another class?", default=default):
        add_class()
    return classes

@time_slot.command()
@click.pass_context
def add(ctx: click.Context) -> None:
    """Add a new time slot."""
    json_config = get_json_config(ctx)
    times = add_timeblock(default=False)
    classes = add_class_pattern(default=False)
    max_time_gap = click.prompt("Max time gap (minutes)", type=int, min=0, default=30)
    min_time_overlap = click.prompt("Min time overlap (minutes)", type=int, min=0, default=45)
    click.echo(
        TimeSlot.add_time_slot(
            json_config=json_config,
            times=times,
            classes=classes,
            max_time_gap=max_time_gap,
            min_time_overlap=min_time_overlap
        )
    )

@time_slot.command()
@click.pass_context
def delete(ctx: click.Context) -> None:
    """Delete a time slot."""
    json_config = get_json_config(ctx)
    if len(json_config.time_slot_config) == 0:
        click.echo("No time slots to delete.")
        return
    click.echo(json_config.time_slot.time_slot_str())
    index = click.prompt("Enter the number time slot to delete" , type=click.IntRange(0, len(json_config.time_slot_config) - 1))
    click.echo(TimeSlot.del_time_slot(json_config=json_config, index=index))
    while click.confirm("Delete another time slot?", default=False):
            click.echo(json_config.time_slot.time_slot_str())
            index = click.prompt("Enter the number time slot to delete",type=click.IntRange(0, len(json_config.time_slot_config) - 1))
            click.echo(TimeSlot.del_time_slot(json_config=json_config, index=index))

@time_slot.command()
@click.pass_context
def modify(ctx: click.Context) -> None:
    """Modify a time slot."""
    json_config = get_json_config(ctx)
    if len(json_config.time_slot_config) == 0:
        click.echo("No time slots to modify..")
        return
    click.echo(json_config.time_slot.time_slot_str())
    index = click.prompt("Enter the number time slot to modify", type=click.IntRange(0, len(json_config.time_slot_config) - 1))
    old_time_slot = json_config.time_slot_config[index]
    if click.confirm("Modify time slot times? (you will create a new set from scratch", default=False):
        new_times = add_timeblock(default=True)
    else:
        new_times = old_time_slot.items

    if click.confirm("Modify time slot classes? (you will create a new set from scratch", default=False):
        new_classes = add_class_pattern(default=True)
    else:
        new_classes = old_time_slot.classes

    max_time_gap = click.prompt("Enter max time gap (minutes)", type=int, min=0, default=old_time_slot.max_time_gap)
    min_time_overlap = click.prompt("Enter min time overlap (minutes)", type=int, min=0, default=old_time_slot.min_time_overlap)
    click.echo(
        TimeSlot.mod_time_slot(
            index=index,
            json_config=json_config,
            times=times,
            classes=classes,
            max_time_gap=max_time_gap,
            min_time_overlap=min_time_overlap
        )
    )



