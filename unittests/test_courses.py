import os
from click.testing import CliRunner
from scheduler_cli import Course, cli

BASE_JSON = os.path.join(os.path.dirname(__file__), "base.json")
CONFIG_KEY: str = "config"

def test_add_course() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", BASE_JSON], obj=obj)
    Course.add_course(obj[CONFIG_KEY], "TEST COURSE", 3, [], [], [], [])
    assert len(obj[CONFIG_KEY].scheduler_config.courses) == 1
    assert obj[CONFIG_KEY].scheduler_config.courses[0].course_id == "TEST COURSE"

def test_del_course() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", BASE_JSON], obj=obj)
    Course.add_course(obj[CONFIG_KEY], "TEST COURSE", 3, [], [], [], [])
    Course.del_course(0, obj[CONFIG_KEY])
    assert len(obj[CONFIG_KEY].scheduler_config.courses) == 0

def test_mod_course() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", BASE_JSON], obj=obj)
    Course.add_course(obj[CONFIG_KEY], "TEST COURSE", 3, [], [], [], [])
    Course.mod_course(0, obj[CONFIG_KEY], "MODIFIED COURSE", 4, [], [], [], [])
    assert len(obj[CONFIG_KEY].scheduler_config.courses) == 1
    assert obj[CONFIG_KEY].scheduler_config.courses[0].course_id == "MODIFIED COURSE"
    assert obj[CONFIG_KEY].scheduler_config.courses[0].credits == 4