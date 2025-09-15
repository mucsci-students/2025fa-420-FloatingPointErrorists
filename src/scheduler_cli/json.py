from scheduler import load_config_from_file, CombinedConfig, SchedulerConfig

class JsonConfig:
    """
    Class to handle loading, saving, and displaying scheduler configuration from a JSON file.

    Attributes:
        file_path (str): The path to the JSON configuration file.
        config (SchedulerConfig): The loaded scheduler configuration.

    If you would like to modify the config in this class, take a look at: https://mucsci.github.io/Scheduler/scheduler.html#SchedulerConfig
    """

    def __init__(self, file_path: str) -> None:
        self._file_path: str = file_path
        self._combinedConfig: CombinedConfig = load_config_from_file(CombinedConfig, file_path)
        self._schedulerConfig: SchedulerConfig = self._combinedConfig.config

    @property
    def config(self) -> SchedulerConfig:
        """The loaded scheduler configuration."""
        return self._schedulerConfig

    @property
    def file_path(self) -> str:
        """The path to the JSON configuration file."""
        return self._file_path

    def save(self) -> None:
        """Save the current configuration back to the JSON file."""
        with open(self._file_path, "w", encoding="utf-8") as file:
            file.write(self._combinedConfig.model_dump_json(indent=4))

    def __str__(self) -> str:
        config = self._schedulerConfig
        lines = ["Rooms:"]
        for room in config.rooms:
            lines.append(f"  - {room}")
        lines.append("\nLabs:")
        for lab in config.labs:
            lines.append(f"  - {lab}")
        lines.append("\nCourses:")
        for course in config.courses:
            lines.append(str(course))
        lines.append("\nFaculty:")
        for faculty in config.faculty:
            lines.append(f"  - {faculty.name}")
            lines.append(f"\tCredits: {faculty.maximum_credits}-{faculty.maximum_credits}")
            lines.append(f"\tUnique course limit: {faculty.unique_course_limit}")
            lines.append("\tTimes:")
            for day in faculty.times:
                lines.append(f"\t{day}: {', '.join(str(t) for t in faculty.times[day])}")
                pass
            if faculty.course_preferences:
                lines.append(f"\tCourse preferences: {faculty.course_preferences}")
            if faculty.room_preferences:
                lines.append(f"\tRoom preferences: {faculty.room_preferences}")
            if faculty.lab_preferences:
                lines.append(f"\tLab preferences: {faculty.lab_preferences}")
        return "\n".join(lines)