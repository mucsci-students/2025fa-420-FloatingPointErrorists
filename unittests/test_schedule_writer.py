import os
import pytest

from scheduler_config_editor.cli.base_cli import run_using_config
from scheduler_config_editor.model import JsonConfig
from scheduler_config_editor.model import ScheduleWriter

SCHEDULES = "schedules"


@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))


@pytest.fixture(scope="session")
def result():
    return {"schedules": []}


class TestRunner:
    def test_write_as_json_creates_file_and_calls_writer(
        self, json_config: JsonConfig, result: dict, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        created = []

        class FakeJSONWriter:
            def __init__(self, path):
                # store absolute path so assertions are stable
                self.path = os.path.abspath(path)
                self.added = []
                created.append(self)

            def __enter__(self):
                # ensure directory and file are created so we can assert on filesystem
                dir_path = os.path.dirname(self.path)
                os.makedirs(dir_path, exist_ok=True)
                open(self.path, "w").close()
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def add_schedule(self, schedule):
                self.added.append(schedule)

        # patch the module where ScheduleWriter looks up JSONWriter
        from scheduler_config_editor.model import schedule_writer as sw

        monkeypatch.setattr(sw, "JSONWriter", FakeJSONWriter)

        # produce schedules using provided fixtures and call writer
        json_config.set_limit(1)
        result[SCHEDULES] = run_using_config(json_config.combined_config)
        ScheduleWriter.write_as_json(result[SCHEDULES], "test_schedule")

        # assertions
        assert len(created) == 1
        expected_path = str(tmp_path / "schedules" / "test_schedule.json")
        assert created[0].path == expected_path
        assert created[0].added == result[SCHEDULES]
        assert (tmp_path / "schedules" / "test_schedule.json").exists()

    def test_write_as_csv_creates_file_and_calls_writer(
        self, json_config: JsonConfig, result: dict, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)
        created = []

        class FakeCSVWriter:
            def __init__(self, path):
                # store absolute path so assertions are stable
                self.path = os.path.abspath(path)
                self.added = []
                created.append(self)

            def __enter__(self):
                # ensure directory and file are created so we can assert on filesystem
                dir_path = os.path.dirname(self.path)
                os.makedirs(dir_path, exist_ok=True)
                open(self.path, "w").close()
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def add_schedule(self, schedule):
                self.added.append(schedule)

        # patch the module where ScheduleWriter looks up JSONWriter
        from scheduler_config_editor.model import schedule_writer as sw

        monkeypatch.setattr(sw, "CSVWriter", FakeCSVWriter)

        # produce schedules using provided fixtures and call writer
        ScheduleWriter.write_as_csv(result[SCHEDULES], "test_schedule")

        # assertions
        assert len(created) == 1
        expected_path = str(tmp_path / "schedules" / "test_schedule.csv")
        assert created[0].path == expected_path
        assert created[0].added == result[SCHEDULES]
        assert (tmp_path / "schedules" / "test_schedule.csv").exists()
