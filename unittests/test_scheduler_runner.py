import os
import pytest

from scheduler_config_editor.model import run_scheduler, JsonConfig
from scheduler_config_editor.model.run_scheduler import (
    run_using_config,
    write_as_json,
    write_as_csv,
)


@pytest.fixture()
def json_config():
    yield JsonConfig(os.path.join(os.path.dirname(__file__), "dummy.json"))


@pytest.fixture(scope="session")
def result():
    return {"result": []}


class TestRunner:
    result = []

    def test_run_using_config_collects_schedules(
        self, json_config: JsonConfig, result: dict
    ):
        json_config.set_limit(1)
        result["result"] = run_using_config(json_config.combined_config)
        assert len(result) == 1  # should collect 5 schedules

    def test_write_as_json_calls_JSONWriter_and_creates_file(
        self, tmp_path, monkeypatch, result: dict
    ):
        # ensure output goes into the temporary directory
        monkeypatch.chdir(tmp_path)

        instances = []

        class DummyJSONWriter:
            def __init__(self, path):
                self.path = path
                self.added = []
                instances.append(self)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def add_schedule(self, schedule):
                self.added.append(schedule)

        monkeypatch.setattr(run_scheduler, "JSONWriter", DummyJSONWriter)

        # call the function under test
        write_as_json(result["result"], "my_schedules")

        # assertions: one writer created, got the schedules, and file exists
        assert len(instances) == 1
        assert instances[0].path == os.path.join("schedules", "my_schedules.json")
        assert instances[0].added == result["result"]
        assert (tmp_path / "schedules" / "my_schedules.json").exists()

    def test_write_as_csv_calls_CSVWriter_and_creates_file(
        self, tmp_path, monkeypatch, result: dict
    ):
        # ensure output goes into the temporary directory
        monkeypatch.chdir(tmp_path)

        instances = []

        class DummyJSONWriter:
            def __init__(self, path):
                self.path = path
                self.added = []
                instances.append(self)

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def add_schedule(self, schedule):
                self.added.append(schedule)

        monkeypatch.setattr(run_scheduler, "CSVWriter", DummyJSONWriter)

        # call the function under test
        write_as_csv(result["result"], "my_schedules")

        # assertions: one writer created, got the schedules, and file exists
        assert len(instances) == 1
        assert instances[0].path == os.path.join("schedules", "my_schedules.csv")
        assert instances[0].added == result["result"]
        assert (tmp_path / "schedules" / "my_schedules.csv").exists()
