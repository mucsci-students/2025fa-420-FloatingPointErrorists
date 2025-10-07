import os

from scheduler import (
    CombinedConfig,
    Scheduler,
    load_config_from_file,
)
from scheduler.writers import JSONWriter, CSVWriter
from scheduler.models import CourseInstance

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
