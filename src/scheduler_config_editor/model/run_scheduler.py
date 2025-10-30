import logging
import os

from alive_progress import alive_bar
from scheduler import (
    CombinedConfig,
    Scheduler,
)
from scheduler.models import CourseInstance
from scheduler.writers import CSVWriter, JSONWriter


def run_using_config(usr_config: CombinedConfig) -> list[list["CourseInstance"]]:
    scheduler = Scheduler(usr_config)
    schedule_list = []
    total = usr_config.limit
    # Temporarily silence all logging
    logging.disable(logging.CRITICAL)
    try:
        with alive_bar(
            total, title="Generating Schedules", bar="bubbles", spinner="crab"
        ) as bar:
            for schedule in scheduler.get_models():
                schedule_list.append(schedule)
                bar()
    finally:
        logging.disable(logging.NOTSET)
    return schedule_list


# write a schedule in json format to data folder
def write_as_json(slist: list[list["CourseInstance"]], name: str) -> None:
    # make new file
    path = os.path.join("schedules", f"{name}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file = open(path, "w")
    # writing for json
    with JSONWriter(path) as writer:
        for schedule in slist:
            writer.add_schedule(schedule)
    file.close()


# write a schedule in json format to data folder
def write_as_csv(slist: list[list["CourseInstance"]], name: str) -> None:
    # make new file
    path = os.path.join("schedules", f"{name}.csv")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file = open(path, "w")
    # writing for csv
    with CSVWriter(path) as writer:
        for schedule in slist:
            writer.add_schedule(schedule)
    file.close()
