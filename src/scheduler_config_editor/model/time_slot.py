from scheduler import TimeString
from scheduler.config import TimeBlock, ClassPattern, Meeting
from scheduler_config_editor.model import JsonConfig
from typing import Literal

DAY = Literal["MON", "TUE", "WED", "THU", "FRI"]
DAY_TO_INDEX: dict[DAY, int] = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5}
INDEX_TO_DAY: dict[int, DAY] = {1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI"}


class TimeSlot:
    """
    This class allows the user to create, modify and delete a time slots from the JsonConfig
    """

    @staticmethod
    def set_max_time_gap(json_config: JsonConfig, max_time_gap: int = 30):
        json_config.time_slot_config.max_time_gap = max_time_gap
        return "Maximum time gap is now " + str(max_time_gap) + " minutes."

    @staticmethod
    def set_min_time_overlap(json_config: JsonConfig, min_time_overlap: int = 45):
        json_config.time_slot_config.min_time_overlap = min_time_overlap
        return "Minimum time overlap is now " + str(min_time_overlap) + " minutes."

    @staticmethod
    def add_time_block(
        json_config: JsonConfig,
        day_index: int,
        start: TimeString,
        spacing: int,
        end: TimeString,
    ) -> str:
        """Adds a time block to the config"""
        day = INDEX_TO_DAY[day_index]
        time_block = TimeBlock(start=start, spacing=spacing, end=end)
        json_config.time_slot_config.times.get(day).append(time_block)
        return "Time block added successfully."

    @staticmethod
    def add_class_pattern(
        json_config: JsonConfig,
        creds: int,
        meetings: list[Meeting],
        disabled: bool,
        start_time: TimeString | None,
    ) -> str:
        """Adds a class pattern to the config"""
        class_pattern = ClassPattern(
            credits=creds, meetings=meetings, disabled=disabled, start_time=start_time
        )
        json_config.time_slot_config.classes.append(class_pattern)
        return "Class pattern added successfully."

    @staticmethod
    def mod_time_block(
        day_index: int,
        index: int,
        json_config: JsonConfig,
        start: TimeString,
        spacing: int,
        end: TimeString,
    ) -> str:
        """Finds time block in config and replaces it with the updated one"""
        day = INDEX_TO_DAY[day_index]
        if index < 0 or index >= len(json_config.time_slot_config.times.get(day, [])):
            raise IndexError("Time block index out of range.")
        old_time_block = json_config.time_slot_config.times.get(day, [])[index]
        time_block = TimeBlock(
            start=start if start is not None else old_time_block.start,
            spacing=spacing if spacing is not None else old_time_block.spacing,
            end=end if end is not None else old_time_block.end,
        )
        json_config.time_slot_config.times.get(day, [])[index] = time_block
        return "Time block updated successfully."

    @staticmethod
    def mod_class_pattern(
        index: int,
        json_config: JsonConfig,
        creds: int,
        meetings: list[Meeting],
        disabled: bool,
        start_time: TimeString | None,
    ) -> str:
        """Finds class pattern in config and replaces it with the updated one"""
        if index < 0 or index >= len(json_config.time_slot_config.classes):
            raise IndexError("Class pattern index out of range.")
        old_class_pattern = json_config.time_slot_config.classes[index]
        class_pattern = ClassPattern(
            credits=creds if creds is not None else old_class_pattern.credits,
            meetings=meetings if meetings is not None else old_class_pattern.meetings,
            disabled=disabled if disabled is not None else old_class_pattern.disabled,
            start_time=start_time
            if start_time is not None
            else old_class_pattern.start_time,
        )
        json_config.time_slot_config.classes[index] = class_pattern
        return "Class pattern updated successfully."

    @staticmethod
    def del_time_block(json_config: JsonConfig, day_index: int, index: int) -> str:
        """Deletes a time block from the config"""
        day = INDEX_TO_DAY[day_index]
        time_blocks = json_config.time_slot_config.times.get(day)
        if time_blocks is None:
            return f"No time block found for day {day}"
        if index < 0 or index >= len(json_config.time_slot_config.times.get(day, [])):
            raise IndexError("Time block index out of range.")
        del time_blocks[index]
        return "Time block deleted successfully."

    @staticmethod
    def del_class_pattern(json_config: JsonConfig, index: int) -> str:
        """Deletes a class pattern from the config"""
        if index < 0 or index >= len(json_config.time_slot_config.classes):
            raise IndexError("Class pattern index out of range.")
        del json_config.time_slot_config.classes[index]
        return "Class pattern deleted successfully."
