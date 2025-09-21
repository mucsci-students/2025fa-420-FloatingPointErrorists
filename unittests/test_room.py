from pathlib import Path
from click.testing import CliRunner
from scheduler_cli import cli, Room

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

def test_room_add_dupe():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    try:
        Room.add_room(jsonObj, "Test Room")
    except ValueError:
        assert jsonObj.scheduler_config.rooms.count("Test Room") == 1

def test_room_del():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    Room.del_room(jsonObj, "Test Room")
    assert jsonObj.scheduler_config.rooms.count("Test Room") == 0

def test_room_del_ne():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Room.del_room(jsonObj, "Test Room")
        assert False
    except ValueError:
        assert True

def test_room_mod():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    Room.mod_room(jsonObj, "Test Room", "New Room")
    assert jsonObj.scheduler_config.rooms.count("New Room") == 1

def test_room_mod_ne():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Room.mod_room(jsonObj, "Test Room", "New Room")
        assert False
    except ValueError:
        assert True
