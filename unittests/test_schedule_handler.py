import json
from scheduler.json_types import CourseInstanceJSON
from scheduler_config_editor.model import ScheduleHandler

course_instance: CourseInstanceJSON = {
    "course": "CS101",
    "faculty": "Dr. Smith",
    "room": "101",
    "lab": "LabA",
    "times": [{"day": 1, "start": 840, "duration": 50}],
    "lab_index": 0
}

def test_import_schedules_json(tmp_path):
    handler = ScheduleHandler()
    json_path = tmp_path / "test.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump([[course_instance]], f)
    handler.import_schedules(str(json_path))
    assert handler.schedules == [[course_instance]]

def test_import_schedules_csv(tmp_path):
    handler = ScheduleHandler()
    csv_path = tmp_path / "test.csv"
    csv_content = "CS101,Dr. Smith,101,LabA,MON 14:00-14:50^\n"
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(csv_content)
    handler.import_schedules(str(csv_path))
    assert handler.schedules[0][0]["course"] == "CS101"

def test_format_schedule():
    result = ScheduleHandler.format_schedule([course_instance])
    assert "CS101" in result
    assert "Dr. Smith" in result

def test_faculty_schedule():
    result = ScheduleHandler.faculty_schedule([course_instance])
    assert "Dr. Smith" in result
    assert "CS101" in result

def test_room_schedule():
    result = ScheduleHandler.room_schedule([course_instance])
    assert "101" in result or "LabA" in result
    assert "CS101" in result
