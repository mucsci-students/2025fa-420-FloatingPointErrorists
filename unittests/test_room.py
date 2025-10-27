from pathlib import Path

from click.testing import CliRunner

from scheduler_config_editor.cli import base_cli
from scheduler_config_editor.model import Room

CONFIG_KEY = "config"
LOAD_COMMAND = "load-config"
# Tests to run: Add new, Try to add duplicate, Delete existing, Delete nonexisting, mod existing, mod non existing


def dummy_path() -> str:
    return str(Path(__file__).parent / "dummy.json")


def test_room_add() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    assert jsonObj.scheduler_config.rooms.count("Test Room") == 1


def test_room_add_dupe() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    try:
        Room.add_room(jsonObj, "Test Room")
    except Room.RoomExistsError:
        assert jsonObj.scheduler_config.rooms.count("Test Room") == 1


def test_room_del() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    Room.del_room(jsonObj, "Test Room")
    assert jsonObj.scheduler_config.rooms.count("Test Room") == 0


def test_room_del_ne() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Room.del_room(jsonObj, "Test Room")
        raise AssertionError()
    except Room.RoomMissingError:
        assert True


def test_room_mod() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "Test Room")
    Room.mod_room(jsonObj, "Test Room", "New Room")
    assert jsonObj.scheduler_config.rooms.count("New Room") == 1


def test_room_mod_ne() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Room.mod_room(jsonObj, "Test Room", "New Room")
        raise AssertionError()
    except Room.RoomMissingError:
        assert True


def test_room_mod_dupe() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Room.add_room(jsonObj, "New Room")
    Room.add_room(jsonObj, "Test Room")
    try:
        Room.mod_room(jsonObj, "Test Room", "New Room")
        raise AssertionError()
    except Room.RoomExistsError:
        assert True
