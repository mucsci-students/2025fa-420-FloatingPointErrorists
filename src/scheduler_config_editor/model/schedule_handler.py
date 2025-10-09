import csv
import json
import os
import re
from scheduler.json_types import CourseInstanceJSON, TimeInstanceJSON
from scheduler.models import CourseInstance
from tabulate import tabulate

DAY_TO_INDEX = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5}
INDEX_TO_DAY = {1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI"}

class ScheduleHandler:
    """
    Handler class for loading, importing, and formatting course schedules.
    This class supports loading schedules from JSON or CSV files, as well as formatting
    schedules into human-readable tables.

    Attributes:
        schedules (list[list[CourseInstanceJSON]]): The loaded schedules.
    """
    def __init__(self):
        self._schedules: list[list[CourseInstanceJSON]] = []

    @property
    def schedules(self) -> list[list[CourseInstanceJSON]]:
        """The loaded schedules."""
        return self._schedules

    def load_schedules(self, schedules: list[list[CourseInstance]]) -> None:
        """Load schedules from a list of CourseInstance lists."""
        for other_schedule in schedules:
            new_schedule = []
            for course_instance in other_schedule:
                new_schedule.append(course_instance.model_dump(by_alias=True, exclude_none=True))
            self._schedules.append(new_schedule)

    def import_schedules(self, file_path: str) -> None:
        """
        Import schedules from a JSON or CSV file. It does not matter whether the file extension is provided or not.
        The method will also determine if the file is in JSON or CSV format.
        """
        possible_paths = [
            file_path,
            f"schedules/{file_path}",
            f"schedules/{file_path}.json",
            f"schedules/{file_path}.csv"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                if path.endswith(".json"):
                    self._load_json_schedules(path)
                    return
                elif path.endswith(".csv"):
                    self._load_csv_schedules(path)
                    return
        raise FileNotFoundError(f"File {file_path} does not exist.")

    def _load_json_schedules(self, file_path: str) -> None:
        """Load schedules from a JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list) or not all(isinstance(s, list) for s in data):
                    raise ValueError("JSON file does not match expected schedule format.")
                self._schedules = data
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {e}")

    def _load_csv_schedules(self, file_path: str) -> None:
        """Load schedules from a CSV file."""
        schedules: list[list[CourseInstanceJSON]] = []
        try:
            with open(file_path, newline='') as csvfile:
                lines = csvfile.read().splitlines()
                blocks = []
                current_block = []
                for line in lines:
                    if line.strip() == "":
                        if current_block:
                            blocks.append(current_block)
                            current_block = []
                    else:
                        current_block.append(line)
                if current_block:
                    blocks.append(current_block)
                for block in blocks:
                    reader = csv.reader(block)
                    schedule = []
                    for row in reader:
                        if not row or not row[0].strip():
                            continue
                        if len(row) < 4:
                            raise ValueError("CSV row does not have enough columns.")
                        course, faculty, room, lab, *times = row
                        lab_index = None
                        time_instances = []
                        for i, time in enumerate(times):
                            if time.endswith('^'): lab_index = i
                            time_instances.append(self._parse_csv_time(time))
                        course_instance: CourseInstanceJSON = {
                            "course": course.strip(),
                            "faculty": faculty.strip(),
                            "room": room.strip() if room.strip() else None,
                            "lab": lab.strip() if lab.strip() else None,
                            "times": time_instances,
                            "lab_index": lab_index
                        }
                        schedule.append(course_instance)
                    schedules.append(schedule)
            self._schedules = schedules
        except Exception as e:
            raise ValueError(f"Invalid CSV format in {file_path}: {e}")

    @staticmethod
    def _parse_csv_time(time_str: str) -> TimeInstanceJSON:
        """Parse a time string in the format "DAY HH:MM-HH:MM" or DAY HH:MM-HH:MM^" into a TimeInstanceJSON."""
        time_str = time_str.rstrip('^')
        match = re.match(r"(\w{3}) (\d{2}):(\d{2})-(\d{2}):(\d{2})", time_str)
        if not match:
            raise ValueError(f"Invalid time format: {time_str}")
        day, start_hour, start_minute, end_hour, end_minute = match.groups()
        day_index = DAY_TO_INDEX[day]
        start = int(start_hour) * 60 + int(start_minute)
        end = int(end_hour) * 60 + int(end_minute)
        duration = end - start
        return {"day": day_index, "start": start, "duration": duration}

    @staticmethod
    def _format_time_instance(time: TimeInstanceJSON) -> str:
        """Format a time instance as 'MON 14:00-14:50'."""
        day_str = INDEX_TO_DAY.get(time["day"])
        start_hour = time["start"] // 60
        start_minute = time["start"] % 60
        end = time["start"] + time["duration"]
        end_hour = end // 60
        end_minute = end % 60
        return f"{day_str} {start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"

    @staticmethod
    def format_schedule(schedule: list[CourseInstanceJSON]) -> str:
        """Format a schedule as a table string."""
        headers = ["Course", "Faculty", "Room", "Lab", "Times", "Lab Index"]
        rows = []
        for course in schedule:
            times_str = " / ".join(ScheduleHandler._format_time_instance(t) for t in course["times"])
            rows.append([
                course.get("course", ""),
                course.get("faculty", ""),
                course.get("room", ""),
                course.get("lab", ""),
                times_str,
                course.get("lab_index", "")
            ])
        return tabulate(rows, headers=headers, tablefmt="grid")

    @staticmethod
    def faculty_schedule(schedule: list[CourseInstanceJSON]) -> str:
        """Format a schedule grouped by faculty as a table string."""
        headers = ["Faculty", "Course", "Room", "Lab", "Times", "Lab Index"]
        sorted_schedule = sorted(schedule, key=lambda c: c.get("faculty", ""))
        rows = []
        for course in sorted_schedule:
            times_str = " / ".join(ScheduleHandler._format_time_instance(t) for t in course["times"])
            rows.append([
                course.get("faculty", ""),
                course.get("course", ""),
                course.get("room", ""),
                course.get("lab", ""),
                times_str,
                course.get("lab_index", "")
            ])
        return tabulate(rows, headers=headers, tablefmt="grid")

    @staticmethod
    def room_schedule(schedule: list[CourseInstanceJSON]) -> str:
        """Format a schedule with separate entries for each room and lab."""
        headers = ["Room/Lab", "Course", "Faculty", "Times", "Lab Index"]
        rows = []
        for course in schedule:
            for loc in [course.get("room", ""), course.get("lab", "")]:
                if loc and loc != "None":
                    times_str = " / ".join(ScheduleHandler._format_time_instance(t) for t in course["times"])
                    rows.append([
                        loc,
                        course.get("course", ""),
                        course.get("faculty", ""),
                        times_str,
                        course.get("lab_index", "")
                    ])
        rows.sort(key=lambda r: r[0])
        return tabulate(rows, headers=headers, tablefmt="grid")