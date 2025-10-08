import csv
import os
from scheduler import (
    CombinedConfig,
    Scheduler,
    load_config_from_file,
)
from scheduler.json_types import CourseInstanceJSON
from scheduler.writers import JSONWriter, CSVWriter
from scheduler.models import CourseInstance

def import_schedules(file_path: str) -> list[list[CourseInstanceJSON]]:
    possible_paths = [
        file_path,
        f"schedules/{file_path}",
        f"schedules/{file_path}.json",
        f"schedules/{file_path}.csv"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            if path.endswith('.json'):
                return load_json_schedules(path)
            elif path.endswith('.csv'):
                return load_csv_schedules(path)
    raise FileNotFoundError(f"File {file_path} does not exist.")

def load_json_schedules(file_path: str) -> list[list[CourseInstanceJSON]]:
    pass

def load_csv_schedules(file_path: str) -> list[list[CourseInstanceJSON]]:
    schedules = []
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
    return schedules

def run_using_config(usr_config: CombinedConfig) -> list[list["CourseInstance"]]:
    # Create scheduler
    scheduler = Scheduler(usr_config)
    scheduleList = []

    # Prints schedules
    for schedule in scheduler.get_models():
        #adds to a list to not repeat calling get_models()
        scheduleList.append(schedule)

    return scheduleList

#write a schedule in json format to data folder
def write_as_json(slist: list[list["CourseInstance"]], name: str) -> None:

    #make new file 
    path = 'schedules/' + name + '.json'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file = open(path, 'w')
    #writing for json
    with JSONWriter(path) as writer:
        for schedule in slist:
            writer.add_schedule(schedule)
    file.close()

#write a schedule in json format to data folder
def write_as_csv(slist: list[list["CourseInstance"]], name: str) -> None:

    #make new file 
    path = 'schedules/' + name + '.csv'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file = open(path, 'w')
    #writing for csv
    with CSVWriter(path) as writer:
        for schedule in slist:
            writer.add_schedule(schedule)
    file.close()
