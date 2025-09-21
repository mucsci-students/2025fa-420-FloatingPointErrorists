import json
from pathlib import Path
from click.testing import CliRunner
from scheduler_cli import cli
from scheduler_cli.room import Room

CONFIG_KEY = "config"

#Tests to run: Add new, Try to add duplicate, Delete existing, Delete nonexisting, mod existing, mod non existing

def dummy_path() -> str:
    return str(Path(__file__).parent / "dummy.json")

def test_room_add():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    assert jsonObj.scheduler_config.rooms.count("Test Room") == 1