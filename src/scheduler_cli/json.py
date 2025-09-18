from scheduler import load_config_from_file, CombinedConfig, SchedulerConfig, TimeSlotConfig

class JsonConfig:
    """
    Class to handle loading, saving, and displaying scheduler configuration from a JSON file.

    Attributes:
        file_path (str): The path to the JSON configuration file.
        scheduler_config (SchedulerConfig): The loaded scheduler configuration.
        time_slot_config (TimeSlotConfig): The loaded time slot configuration.
        combined_config (CombinedConfig): The loaded combined configuration.

    If you would like to modify the config in this class, take a look at: https://mucsci.github.io/Scheduler/scheduler.html#SchedulerConfig
    """

    def __init__(self, file_path: str) -> None:
        self._file_path: str = file_path
        self._combined_config: CombinedConfig = load_config_from_file(CombinedConfig, file_path)
        self._scheduler_config: SchedulerConfig = self._combined_config.config
        self._time_slot_config: TimeSlotConfig = self._combined_config.time_slot_config

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

    def _scheduler_str(self) -> str:
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
            lines.append(f"\tCredits: {faculty.maximum_credits}-{faculty.maximum_credits}")
            lines.append(f"\tUnique course limit: {faculty.unique_course_limit}")
            lines.append("\tTimes:")
            for day in faculty.times:
                lines.append(f"\t  {day}: {', '.join(str(t) for t in faculty.times[day])}")
            if faculty.course_preferences:
                lines.append(f"\tCourse preferences: {faculty.course_preferences}")
            if faculty.room_preferences:
                lines.append(f"\tRoom preferences: {faculty.room_preferences}")
            if faculty.lab_preferences:
                lines.append(f"\tLab preferences: {faculty.lab_preferences}")
        return "\n".join(lines)

    def _time_slot_str(self) -> str:
        """String representation of the time slot configuration."""
        time_slot_config = self._time_slot_config
        lines = ["\nTime Slot Config:"]
        for day, slots in time_slot_config.times.items():
            lines.append(f"  {day}:")
            for slot in slots:
                lines.append(f"    - Start: {slot.start}, End: {slot.end}, Spacing: {slot.spacing}")
        lines.append("\nClasses:")
        for cls in time_slot_config.classes:
            meetings_str = ", ".join(
                f"{m.day} (Duration={m.duration}, lab={getattr(m, 'lab', False)})"
                for m in cls.meetings
            )
            lines.append(f"  - Credits: {cls.credits}, Meetings: [{meetings_str}]")
        return "\n".join(lines)

    def __str__(self) -> str:
        """String representation of the entire configuration."""
        combined_config = self._combined_config
        lines = [self._scheduler_str(), self._time_slot_str(), f"\nLimit: {getattr(combined_config, 'limit', None)}",
                 "\nOptimizer Flags:"]
        for flag in getattr(combined_config, "optimizer_flags", []):
            lines.append(f"  - {flag}")
        return "\n".join(lines)