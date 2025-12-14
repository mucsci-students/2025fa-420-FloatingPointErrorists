import os
import copy
from enum import Enum
from typing import Literal, List

from scheduler import (
    CombinedConfig,
    OptimizerFlags,
    SchedulerConfig,
    TimeSlotConfig,
    load_config_from_file,
)

DAYS = Literal["MON", "TUE", "WED", "THU", "FRI"]
DayList: List[DAYS] = ["MON", "TUE", "WED", "THU", "FRI"]


class JsonConfig:
    """
    Class to handle loading, saving, and displaying scheduler configuration from a JSON file.

    Attributes:
        file_path (str): The path to the JSON configuration file.
        scheduler_config (SchedulerConfig): The loaded scheduler configuration.
        time_slot_config (TimeSlotConfig): The loaded time slot configuration.
        combined_config (CombinedConfig): The loaded combined configuration.

    If you would like to modify the scheduler config in this class, take a look at: https://mucsci.github.io/Scheduler/scheduler.html#SchedulerConfig
    """

    class Mode(Enum):
        """Modes for JsonConfig operations."""

        CREATE = 0
        LOAD = 1

    def __init__(self, file_path: str, mode: Mode = Mode.LOAD) -> None:
        """Initialize the JsonConfig with the path to the JSON file."""
        if not file_path.endswith(".json"):
            file_path += ".json"
        if not os.path.isabs(file_path) and not os.path.exists(file_path):
            file_path = os.path.join("configs", file_path)
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        self._file_path = (
            file_path
            if mode == JsonConfig.Mode.LOAD
            else JsonConfig._create_config(file_path)
        )
        if not os.path.exists(self._file_path):
            raise FileNotFoundError(
                f"Configuration file {self._file_path} does not exist."
            )
        self._combined_config: CombinedConfig = load_config_from_file(
            CombinedConfig, self._file_path
        )
        self.__undo_stack: list[CombinedConfig] = []
        self.__redo_stack: list[CombinedConfig] = []
        self._scheduler_config: SchedulerConfig = self._combined_config.config
        self._time_slot_config: TimeSlotConfig = self._combined_config.time_slot_config

    @staticmethod
    def _create_config(file_path: str) -> str:
        with open("data/default.json", encoding="utf-8") as default_config:
            default_data = default_config.read()
        with open(file_path, "w", encoding="utf-8") as target_file:
            target_file.write(default_data)
        return file_path

    def _load_config(self):
        pass

    @property
    def scheduler_config(self) -> SchedulerConfig:
        """The loaded scheduler configuration."""
        return self._scheduler_config

    @property
    def time_slot_config(self) -> TimeSlotConfig:
        """The loaded time slot configuration."""
        return self._time_slot_config

    @property
    def combined_config(self) -> CombinedConfig:
        """The loaded combined configuration."""
        return self._combined_config

    @property
    def file_path(self) -> str:
        """The path to the JSON configuration file."""
        return self._file_path

    def save(self) -> None:
        """Save the current configuration back to the JSON file."""
        with open(self._file_path, "w", encoding="utf-8") as file:
            file.write(self._combined_config.model_dump_json(indent=4))

    def set_limit(self, limit: int) -> None:
        """Set the limit for the scheduler"""
        if limit <= 0:
            raise ValueError("Limit must be a positive integer.")
        self._combined_config.limit = limit

    def set_optimization(self, optimizer_list: list[OptimizerFlags]) -> None:
        """Set the optimizer flags"""
        self._combined_config.optimizer_flags = optimizer_list

    def scheduler_str(self) -> str:
        """String representation of the scheduler configuration."""
        scheduler_config = self._scheduler_config
        lines = ["Rooms:"]
        for room in scheduler_config.rooms:
            lines.append(f"  - {room}")
        lines.append("\nLabs:")
        for lab in scheduler_config.labs:
            lines.append(f"  - {lab}")
        lines.append("\nCourses:")
        for course in scheduler_config.courses:
            lines.append(f"  - {course}")
        lines.append("\nFaculty:")
        for faculty in scheduler_config.faculty:
            lines.append(f"  - {faculty.name}")
            lines.append(
                f"\tCredits: {faculty.minimum_credits}-{faculty.maximum_credits}"
            )
            lines.append(f"\tUnique course limit: {faculty.unique_course_limit}")
            lines.append("\tTimes:")
            for day in faculty.times:
                lines.append(
                    f"\t  {day}: {', '.join(str(t) for t in faculty.times[day])}"
                )
            if faculty.course_preferences:
                lines.append(f"\tCourse preferences: {faculty.course_preferences}")
            if faculty.room_preferences:
                lines.append(f"\tRoom preferences: {faculty.room_preferences}")
            if faculty.lab_preferences:
                lines.append(f"\tLab preferences: {faculty.lab_preferences}")
        return "\n".join(lines)

    def time_slot_str(self) -> str:
        """String representation of the time slot configuration."""
        time_slot_config = self._time_slot_config
        lines = self.time_block_str() + self.class_pattern_str()
        lines += f"\nMax Time Gap: {time_slot_config.max_time_gap}"
        lines += f"\nMin Time Overlap: {time_slot_config.min_time_overlap}"
        return lines

    def time_block_str(self) -> str:
        """String representation of the time block configuration."""
        time_slot_config = self._time_slot_config
        lines = ["\nTime Slot Config:"]
        for day in DayList:
            slots = time_slot_config.times.get(day, [])
            lines.append(f"  {day}:")
            if not slots:
                lines.append("")
            else:
                for i, slot in enumerate(slots):
                    lines.append(
                        f"    [{i}]- Start: {slot.start}, End: {slot.end}, Spacing: {slot.spacing}"
                    )
        return "\n".join(lines)

    def class_pattern_str(self) -> str:
        """String representation of the class pattern configuration."""
        time_slot_config = self._time_slot_config
        lines = ["\nClasses:"]
        if not time_slot_config.classes:
            lines.append("")
        else:
            for i, cls in enumerate(time_slot_config.classes):
                meetings_str = ", ".join(
                    f"{m.day} (Duration={m.duration}, lab={getattr(m, 'lab', False)})"
                    for m in cls.meetings
                )
                lines.append(
                    f" [{i}] - Credits: {cls.credits}, Meetings: [{meetings_str}], Disabled:{cls.disabled}"
                )
        return "\n".join(lines)

    def __str__(self) -> str:
        """String representation of the entire configuration."""
        combined_config = self._combined_config
        lines = [
            self.scheduler_str(),
            f"\nLimit: {getattr(combined_config, 'limit', None)}",
            "\nOptimizer Flags:",
        ]
        for flag in getattr(combined_config, "optimizer_flags", []):
            lines.append(f"  - {flag}")
        return "\n".join(lines)

    # Undo button is pressed
    def undo(self) -> None:
        if self.__undo_stack.__len__() == 0:
            raise IndexError("No changes to undo.")

        # Save current state to redo
        self.__redo_stack.append(copy.deepcopy(self._combined_config))

        # Restore previous state
        prev = self.__undo_stack.pop()
        self._combined_config = prev
        self._scheduler_config = prev.config
        self._time_slot_config = prev.time_slot_config

    # Redo button is pressed
    def redo(self) -> None:
        if self.__redo_stack.__len__() == 0:
            raise IndexError("No changes to redo.")

        # Save current state to undo
        self.__undo_stack.append(copy.deepcopy(self._combined_config))

        # Restore next state
        next_state = self.__redo_stack.pop()
        self._combined_config = next_state
        self._scheduler_config = next_state.config
        self._time_slot_config = next_state.time_slot_config

    # Called when a change is made to the config and saved, meaning we should push our old config onto the stack
    def add_to_undo_stack(self):
        self.__undo_stack.append(copy.deepcopy(self._combined_config))
        self.__redo_stack.clear()

    def get_undo_stack_size(self) -> int:
        return len(self.__undo_stack)

    def get_redo_stack_size(self) -> int:
        return len(self.__redo_stack)

    def clear_stacks(self) -> None:
        self.__undo_stack.clear()
        self.__redo_stack.clear()
