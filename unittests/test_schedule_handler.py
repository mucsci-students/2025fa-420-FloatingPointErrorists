# language: python
import sys
from pathlib import Path
import json
import csv
import os
import re
import io
import pytest

# Ensure project's src is importable (adjust relative to tests directory)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from scheduler_config_editor.model.schedule_handler import ScheduleHandler


class DummyCourseInstance:
    """Minimal stand-in for CourseInstance with model_dump."""
    def __init__(self, data):
        self._data = data

    def model_dump(self, by_alias=True, exclude_none=True):
        return self._data


def test_load_schedules_and_schedule_rows():
    handler = ScheduleHandler()
    data = {
        "course": "CS101",
        "faculty": "Dr. A",
        "room": "R1",
        "lab": None,
        "times": [{"day": 1, "start": 9 * 60, "duration": 50}],
        "lab_index": None,
    }
    handler.load_schedules([[DummyCourseInstance(data)]])
    assert isinstance(handler.schedules, list)
    assert handler.schedules[0][0]["course"] == "CS101"

    # schedule_rows and format output check
    rows = handler.schedule_rows(handler.schedules[0])
    assert rows[0][0] == "CS101"
    s = handler.format_schedule_str(handler.schedules[0])
    assert "CS101" in s and "Dr. A" in s


def test_parse_csv_time_and_format_time():
    # valid parse
    t = ScheduleHandler._parse_csv_time("MON 09:00-10:00")
    assert t["day"] == 1
    assert t["start"] == 9 * 60
    assert t["duration"] == 60

    # format_time_instance
    fmt = ScheduleHandler._format_time_instance(t)
    assert fmt.startswith("MON 09:00-10:00")

    # invalid parse raises
    with pytest.raises(ValueError):
        ScheduleHandler._parse_csv_time("INVALID STRING")


def test_split_blocks_and_parse_block_and_csv_roundtrip(tmp_path):
    csv_content_block1 = [
        ["CS101", "Dr. A", "R1", "None", "MON 09:00-09:50", "WED 09:00-09:50^"],
    ]
    csv_content_block2 = [
        ["MA201", "Dr. B", "R2", "L1", "TUE 10:00-11:00^"],
    ]
    # write CSV file lines with a blank line between blocks
    file_lines = []
    for row in csv_content_block1:
        file_lines.append(",".join(row))
    file_lines.append("")  # separator
    for row in csv_content_block2:
        file_lines.append(",".join(row))
    csv_file = tmp_path / "schedules.csv"
    csv_file.write_text("\n".join(file_lines))

    handler = ScheduleHandler()
    handler._load_csv_schedules(str(csv_file))

    # two schedules (two blocks)
    assert len(handler.schedules) == 2
    s1 = handler.schedules[0][0]
    # lab detection: '^' was on the second time for CS101 -> lab_index == 1
    assert s1["lab_index"] == 1
    # times parsed
    assert any(t["day"] == 1 for t in s1["times"])  # MON in block1
    # Check second block parsed
    s2 = handler.schedules[1][0]
    assert s2["course"] == "MA201"


def test_load_csv_schedules_raises_when_parse_block_fails(tmp_path, monkeypatch):
    # Create a valid CSV file but monkeypatch _parse_block to raise
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("A,B,C,D,MON 09:00-10:00\n")
    monkeypatch.setattr(ScheduleHandler, "_parse_block", staticmethod(lambda x: (_ for _ in ()).throw(Exception("boom"))))
    handler = ScheduleHandler()
    with pytest.raises(ValueError) as excinfo:
        handler._load_csv_schedules(str(csv_file))
    assert "Invalid CSV format" in str(excinfo.value)


def test_load_json_schedules_valid_and_invalid(tmp_path):
    handler = ScheduleHandler()
    good = tmp_path / "good.json"
    bad = tmp_path / "bad.json"
    good.write_text(json.dumps([[{"course": "CS101", "faculty": "F"}]]))
    bad.write_text("not a json")

    # valid
    handler._load_json_schedules(str(good))
    assert handler.schedules[0][0]["course"] == "CS101"

    # invalid
    with pytest.raises(ValueError) as excinfo:
        handler._load_json_schedules(str(bad))
    assert "Invalid JSON format" in str(excinfo.value)


def test_import_schedules_variants(tmp_path):
    # create multiple candidate files and ensure import picks correct one
    base = tmp_path / "schedules"
    base.mkdir()
    # create schedules/foo.csv and schedules/foo.json
    csvf = base / "foo.csv"
    jsonf = base / "foo.json"
    csvf.write_text("CS101,Dr. A,R1,None,MON 09:00-09:50\n")
    jsonf.write_text(json.dumps([[{"course": "JX", "faculty": "Y"}]]))

    handler = ScheduleHandler()
    # import by name should find schedules/foo.json (search order tries exact path then schedules/... then .json, .csv)
    # To exercise different branch, call with full path to csvf to choose CSV branch
    handler.import_schedules(str(csvf))
    assert handler.schedules[0][0]["course"] == "CS101"

    # import by base name should find schedules/foo.json (since exists)
    # handler.import_schedules("foo")
    # # after previous import, schedules replaced by JSON content
    # assert handler.schedules[0][0]["course"] == "JX"

    # missing file raises
    with pytest.raises(FileNotFoundError):
        handler.import_schedules("does_not_exist_zzz")


def test_faculty_and_room_rows_and_strings():
    handler = ScheduleHandler()
    course = {
        "course": "CS101",
        "faculty": "ProfX",
        "room": "R1",
        "lab": "L1",
        "times": [
            {"day": 1, "start": 8 * 60, "duration": 50},
            {"day": 3, "start": 10 * 60, "duration": 50},
        ],
        "lab_index": 1,
    }
    schedule = [course]
    # rows
    fac_rows = ScheduleHandler.faculty_schedule_rows(schedule)
    assert any("ProfX" in r[0] or "ProfX" in r[1] for r in fac_rows)
    room_rows = ScheduleHandler.room_schedule_rows(schedule)
    # There should be rows for both R1 and L1
    rooms_present = {r[0] for r in room_rows}
    assert "R1" in rooms_present and "L1" in rooms_present

    # string formatting functions
    fs = ScheduleHandler.faculty_schedule_str(schedule)
    rs = ScheduleHandler.room_schedule_str(schedule)
    assert "ProfX" in fs
    assert "R1" in rs and "L1" in rs
