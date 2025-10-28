import os
from typing import cast, Any

from scheduler_config_editor.model import run_scheduler


def test_run_using_config_collects_schedules(monkeypatch):
    created = []

    class FakeScheduler:
        def __init__(self, cfg):
            self.cfg = cfg
            created.append(self)

        def get_models(self):
            return [["ci1", "ci2"], ["ci3"]]

    monkeypatch.setattr(run_scheduler, "Scheduler", FakeScheduler)

    result = run_scheduler.run_using_config(cast(Any, object()))
    assert result == [["ci1", "ci2"], ["ci3"]]
    assert len(created) == 1  # constructor was called exactly once


def test_write_as_json_calls_JSONWriter_and_creates_file(tmp_path, monkeypatch):
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

    schedules = [["s1"], ["s2", "s3"]]
    run_scheduler.write_as_json(cast(Any, schedules), "my_schedule")

    assert len(instances) == 1
    assert instances[0].path == os.path.join("schedules", "my_schedule.json")
    assert instances[0].added == schedules
    assert (tmp_path / "schedules" / "my_schedule.json").exists()


def test_write_as_csv_calls_CSVWriter_and_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    instances = []

    class DummyCSVWriter:
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

    monkeypatch.setattr(run_scheduler, "CSVWriter", DummyCSVWriter)

    schedules = [["c1"], ["c2", "c3"]]
    run_scheduler.write_as_csv(cast(Any, schedules), "csv_schedule")

    assert len(instances) == 1
    assert instances[0].path == os.path.join("schedules", "csv_schedule.csv")
    assert instances[0].added == schedules
    assert (tmp_path / "schedules" / "csv_schedule.csv").exists()
