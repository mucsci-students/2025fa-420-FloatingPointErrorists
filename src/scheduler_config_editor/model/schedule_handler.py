import csv
import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, cast, Tuple

from scheduler.json_types import CourseInstanceJSON, TimeInstanceJSON
from scheduler.models import CourseInstance
from tabulate import tabulate

DAY_TO_INDEX = {"MON": 1, "TUE": 2, "WED": 3, "THU": 4, "FRI": 5}
INDEX_TO_DAY = {1: "MON", 2: "TUE", 3: "WED", 4: "THU", 5: "FRI"}
DAYS = ["MON", "TUE", "WED", "THU", "FRI"]


@dataclass
class CourseMeeting:
    name: str
    time: Tuple[int, int]
    room: str
    faculty: str


class ScheduleHandler:
    """
    Handler class for loading, importing, and formatting course schedules.
    This class supports loading schedules from JSON or CSV files, as well as formatting
    schedules into human-readable tables.

    Attributes:
        schedules (list[list[CourseInstanceJSON]]): The loaded schedules.
    """

    def __init__(self) -> None:
        self._schedules: list[list[CourseInstanceJSON]] = []

    @property
    def schedules(self) -> list[list[CourseInstanceJSON]]:
        """The loaded schedules."""
        return self._schedules

    def load_schedules(self, schedules: list[list[CourseInstance]]) -> None:
        """Load schedules from a list of CourseInstance lists."""
        self._schedules = [
            [ci.model_dump(by_alias=True, exclude_none=True) for ci in sched]
            for sched in schedules
        ]

    def import_schedules(self, file_path: str) -> None:
        """
        Import schedules from a JSON or CSV file. It does not matter whether the file extension is provided or not.
        The method will also determine if the file is in JSON or CSV format.
        """
        possible_paths = [
            file_path,
            f"schedules/{file_path}",
            f"schedules/{file_path}.json",
            f"schedules/{file_path}.csv",
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
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list) or not all(
                    isinstance(s, list) for s in data
                ):
                    raise ValueError(
                        "JSON file does not match expected schedule format."
                    )
                self._schedules = data
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {e}") from e

    def _load_csv_schedules(self, file_path: str) -> None:
        """Load schedules from a CSV file."""
        try:
            with open(file_path, newline="") as csvfile:
                lines = csvfile.read().splitlines()
            blocks = ScheduleHandler._split_blocks(lines)
            schedules = [ScheduleHandler._parse_block(block) for block in blocks]
            self._schedules = schedules
        except Exception as e:
            raise ValueError(f"Invalid CSV format in {file_path}: {e}") from e

    @staticmethod
    def _split_blocks(lines: list[str]) -> list[list[str]]:
        """Split lines into blocks separated by empty lines."""
        blocks: list[list[str]] = []
        current_block: list[str] = []
        for line in lines:
            if line.strip() == "":
                if current_block:
                    blocks.append(current_block)
                    current_block = []
            else:
                current_block.append(line)
        if current_block:
            blocks.append(current_block)
        return blocks

    @staticmethod
    def _parse_block(block: list[str]) -> list[CourseInstanceJSON]:
        """Parse a block of CSV lines into a list of CourseInstanceJSON."""
        schedule = []
        reader = csv.reader(block)
        for row in reader:
            if not row or not row[0].strip():
                continue
            if len(row) < 4:
                raise ValueError("CSV row does not have enough columns.")
            course, faculty, room, lab, *times = row
            lab_index = None
            time_instances = []
            for i, time in enumerate(times):
                if time.endswith("^"):
                    lab_index = i
                time_instances.append(ScheduleHandler._parse_csv_time(time))
            course_instance: CourseInstanceJSON = {
                "course": course.strip(),
                "faculty": faculty.strip(),
                "room": room.strip() if room.strip() and room != "None" else None,
                "lab": lab.strip() if lab.strip() and lab != "None" else None,
                "times": time_instances,
                "lab_index": lab_index,
            }
            schedule.append(course_instance)
        return schedule

    @staticmethod
    def _parse_csv_time(time_str: str) -> TimeInstanceJSON:
        """Parse a time string in the format "DAY HH:MM-HH:MM" or DAY HH:MM-HH:MM^" into a TimeInstanceJSON."""
        time_str = time_str.rstrip("^")
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
        day = INDEX_TO_DAY[time["day"]]
        start_hour = time["start"] // 60
        start_minute = time["start"] % 60
        end = time["start"] + time["duration"]
        end_hour = end // 60
        end_minute = end % 60
        return (
            f"{day} {start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"
        )

    @staticmethod
    def _group_by_faculty(
        schedule: list[CourseInstanceJSON],
    ) -> dict[Any, list[CourseInstanceJSON]]:
        """Group courses in the schedule by faculty."""
        faculty_map: dict[Any, list[CourseInstanceJSON]] = defaultdict(list)
        for course in schedule:
            faculty_map[course["faculty"]].append(course)
        return faculty_map

    @staticmethod
    def _group_by_room(
        schedule: list[CourseInstanceJSON],
    ) -> dict[Any, list[CourseInstanceJSON]]:
        """Group courses in the schedule by room."""
        room_map: dict[Any, list[CourseInstanceJSON]] = defaultdict(list)
        for course in schedule:
            if course.get("room") is not None:
                room_map[course["room"]].append(course)
            if course.get("lab") is not None:
                room_map[course["lab"]].append(course)
        return room_map

    @staticmethod
    def _avg_start(course: CourseInstanceJSON) -> float:
        """Get the average start time across all meeting times for a course, or +inf if none."""
        starts = [t["start"] for t in course.get("times", [])]
        return sum(starts) / len(starts) if starts else float("inf")

    @staticmethod
    def _faculty_row(course: CourseInstanceJSON, days: list[str]) -> list[str]:
        """Build a row for a faculty schedule table."""
        lab_index = course.get("lab_index")
        row = [course["course"], f"{course.get('room', '')} ({course.get('lab', '')})"]
        for day in days:
            meetings = [
                ScheduleHandler._format_time_instance(time)
                + ("^" if lab_index is not None and idx == lab_index else "")
                for idx, time in enumerate(course["times"])
                if INDEX_TO_DAY[time["day"]] == day
            ]
            meeting_str = ", ".join(m[4:] for m in meetings)
            row.append(meeting_str)
        return row

    @staticmethod
    def _room_row(course: CourseInstanceJSON, days: list[str], room: str) -> list[str]:
        """Build a row for a room schedule table."""
        lab_index = course.get("lab_index")
        row = [course["course"], course["faculty"]]
        for day in days:
            meetings = [
                ScheduleHandler._format_time_instance(time)[4:]
                for idx, time in enumerate(course["times"])
                if INDEX_TO_DAY[time["day"]] == day
                and (
                    (room == course.get("lab") and idx == lab_index)
                    or (room == course.get("room") and idx != lab_index)
                )
            ]
            row.append(", ".join(meetings))
        return row

    @staticmethod
    def _day_column(courses: list[CourseInstanceJSON]) -> list[list[CourseMeeting]]:
        """Build a column for a faculty schedule table."""
        meetings: list[list[CourseMeeting]] = [[] for _ in range(5)]
        for course in courses:
            lab_index = course.get("lab_index")
            for idx, time in enumerate(course["times"]):
                meeting = (time["start"], time["start"] + time["duration"])
                room = course["lab"] if idx == lab_index else course["room"]
                meetings[time["day"] - 1].append(
                    CourseMeeting(
                        name=course["course"],
                        time=meeting,
                        room=room if room is not None else "",
                        faculty=course["faculty"],
                    )
                )
        return meetings

    @staticmethod
    def schedule_rows(schedule: list[CourseInstanceJSON]) -> list[list[str]]:
        """Build rows for the general schedule table."""
        rows: list[list[str]] = []
        for course in schedule:
            lab_index = course.get("lab_index")
            time_str = ", ".join(
                ScheduleHandler._format_time_instance(t)
                + ("^" if lab_index is not None and idx == lab_index else "")
                for idx, t in enumerate(course["times"])
            )
            row = [
                course["course"],
                course["faculty"],
                course.get("room", ""),
                course.get("lab", ""),
                time_str,
            ]
            rows.append(cast(list[str], row))
        return rows

    @staticmethod
    def faculty_schedule_columns(
        schedule: list[CourseInstanceJSON],
    ) -> list[tuple[str, list[list[CourseMeeting]]]]:
        """Build Columns for the faculty schedule table."""
        faculty_map = ScheduleHandler._group_by_faculty(schedule)
        return [
            (
                faculty,
                ScheduleHandler._day_column(
                    sorted(courses, key=ScheduleHandler._avg_start)
                ),
            )
            for faculty, courses in faculty_map.items()
        ]

    @staticmethod
    def room_schedule_columns(
        schedule: list[CourseInstanceJSON],
    ) -> list[tuple[str, list[list[CourseMeeting]]]]:
        """Build Columns for the room schedule table."""
        room_map = ScheduleHandler._group_by_room(schedule)
        return [
            (
                room,
                ScheduleHandler._day_column(
                    sorted(courses, key=ScheduleHandler._avg_start)
                ),
            )
            for room, courses in room_map.items()
        ]

    @staticmethod
    def format_schedule_str(schedule: list[CourseInstanceJSON]) -> str:
        """Format the general schedule as a table string."""
        headers = ["Course", "Faculty", "Room", "Lab", "Times"]
        return tabulate(
            ScheduleHandler.schedule_rows(schedule), headers=headers, tablefmt="github"
        )

    @staticmethod
    def faculty_schedule_str(schedule: list[CourseInstanceJSON]) -> str:
        """Format the faculty schedule as a table string."""
        faculty_map = ScheduleHandler._group_by_faculty(schedule)
        out = ""
        for faculty, courses in faculty_map.items():
            out += f"\n{faculty}:\n"
            headers = ["Course", "Room (Lab)"] + DAYS
            rows = [
                ScheduleHandler._faculty_row(c, DAYS)
                for c in sorted(courses, key=ScheduleHandler._avg_start)
            ]
            out += tabulate(rows, headers=headers, tablefmt="github") + "\n"
        return out

    @staticmethod
    def room_schedule_str(schedule: list[CourseInstanceJSON]) -> str:
        """Format the room schedule as a table string."""
        room_map = ScheduleHandler._group_by_room(schedule)
        out = ""
        for room, courses in room_map.items():
            out += f"\n{room}:\n"
            headers = ["Course", "Faculty"] + DAYS
            rows = [
                ScheduleHandler._room_row(c, DAYS, room)
                for c in sorted(courses, key=ScheduleHandler._avg_start)
            ]
            out += tabulate(rows, headers=headers, tablefmt="github") + "\n"
        return out
