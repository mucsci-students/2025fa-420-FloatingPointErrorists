import csv
import json
import os
import re
from collections import defaultdict
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
    def __init__(self) -> None:
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
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list) or not all(isinstance(s, list) for s in data):
                    raise ValueError("JSON file does not match expected schedule format.")
                self._schedules = data
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {e}") from e

    def _load_csv_schedules(self, file_path: str) -> None:
        """Load schedules from a CSV file."""
        try:
            with open(file_path, newline='') as csvfile:
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
                if time.endswith('^'):
                    lab_index = i
                time_instances.append(ScheduleHandler._parse_csv_time(time))
            course_instance: CourseInstanceJSON = {
                "course": course.strip(),
                "faculty": faculty.strip(),
                "room": room.strip() if room.strip() else None,
                "lab": lab.strip() if lab.strip() else None,
                "times": time_instances,
                "lab_index": lab_index
            }
            schedule.append(course_instance)
        return schedule

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
        day = INDEX_TO_DAY[time["day"]]
        start_hour = time["start"] // 60
        start_minute = time["start"] % 60
        end = time["start"] + time["duration"]
        end_hour = end // 60
        end_minute = end % 60
        return f"{day} {start_hour:02d}:{start_minute:02d}-{end_hour:02d}:{end_minute:02d}"

    @staticmethod
    def format_schedule(schedule: list[CourseInstanceJSON]) -> str:
        """Returns a string of the schedule formatted as a table."""
        headers = ["Course", "Faculty", "Room", "Lab", "Times"]
        rows = []
        for course in schedule:
            lab_index = course.get("lab_index")
            time_str = ", ".join(
                ScheduleHandler._format_time_instance(t) + ("^" if lab_index is not None and idx == lab_index else "")
                for idx, t in enumerate(course["times"])
            )
            row = [
                course["course"],
                course["faculty"],
                course.get("room", ""),
                course.get("lab", ""),
                time_str,
            ]
            rows.append(row)
        return tabulate(rows, headers=headers, tablefmt="github")

    @staticmethod
    def faculty_schedule(schedule: list[CourseInstanceJSON]) -> str:
        """Returns s string of the schedule where each faculty has their own table with days as columns."""
        days = ["MON", "TUE", "WED", "THU", "FRI"]
        faculty_map = defaultdict(list)
        for course in schedule:
            faculty_map[course["faculty"]].append(course)
        final_str = ""
        for faculty, courses in faculty_map.items():
            final_str += f"\n{faculty}:\n"
            headers = ["Course", "Room (Lab)"] + days
            rows = []
            for course in courses:
                lab_index = course.get("lab_index")
                row = [
                    course["course"],
                    f"{course.get('room', '')} ({course.get('lab', '')})"
                ]
                for day in days:
                    meetings = [
                        ScheduleHandler._format_time_instance(time) + (
                            "^" if lab_index is not None and idx == lab_index else "")
                        for idx, time in enumerate(course["times"])
                        if INDEX_TO_DAY[time["day"]] == day
                    ]
                    meeting_str = ", ".join(m[4:] for m in meetings)
                    row.append(meeting_str)
                rows.append(row)
            final_str += tabulate(rows, headers=headers, tablefmt="github") + "\n"
        return final_str

    @staticmethod
    def room_schedule(schedule: list[CourseInstanceJSON]) -> str:
        """Returns a string of the schedule where each room has its own table with days as columns."""
        days = ["MON", "TUE", "WED", "THU", "FRI"]
        room_map = defaultdict(list)
        for course in schedule:
            room = course.get("room")
            lab = course.get("lab")
            if room is not None:
                room_map[room].append(course)
            if lab is not None:
                room_map[lab].append(course)
        final_str = ""
        for room, courses in room_map.items():
            final_str += f"\n{room}:\n"
            headers = ["Course", "Faculty"] + days
            rows = []
            for course in courses:
                lab_index = course.get("lab_index")
                row = [course["course"], course["faculty"]]
                for day in days:
                    meetings = [
                        ScheduleHandler._format_time_instance(time)[4:]
                        for idx, time in enumerate(course["times"])
                        if INDEX_TO_DAY[time["day"]] == day and (
                                (room == course.get("lab") and idx == lab_index) or
                                (room == course.get("room") and idx != lab_index)
                        )
                    ]
                    row.append(", ".join(meetings))
                rows.append(row)
            final_str += tabulate(rows, headers=headers, tablefmt="github") + "\n"
        return final_str