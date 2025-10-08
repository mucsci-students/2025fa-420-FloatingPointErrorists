import csv
import os
from scheduler.json_types import CourseInstanceJSON

DAY_TO_INDEX = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4}

def import_schedules(file_path: str) -> list[list[CourseInstanceJSON]]:
    possible_paths = [
        file_path,
        f"schedules/{file_path}",
        f"schedules/{file_path}.json",
        f"schedules/{file_path}.csv"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            if path.endswith(".json"):
                return load_json_schedules(path)
            elif path.endswith(".csv"):
                return load_csv_schedules(path)
    raise FileNotFoundError(f"File {file_path} does not exist.")

def load_json_schedules(file_path: str) -> list[list[CourseInstanceJSON]]:
    pass

def load_csv_schedules(file_path: str) -> list[list[CourseInstanceJSON]]:
    schedules: list[list[CourseInstanceJSON]] = []
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
                course, faculty, room, lab, *times = row
                lab_index = None
                for i, time in enumerate(times):
                    if time.endswith('^') lab_index = i
    return schedules