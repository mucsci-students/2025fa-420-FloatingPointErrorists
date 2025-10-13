from pathlib import Path
from click.testing import CliRunner
from scheduler_config_editor.cli import base_cli
from scheduler_config_editor.model import Lab

CONFIG_KEY = "config"
LOAD_COMMAND = "load-config"
#Tests to run: Add new, Try to add duplicate, Delete existing, Delete nonexisting, mod existing, mod non existing

def dummy_path() -> str:
    return str(Path(__file__).parent / "dummy.json")

def test_lab_add() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    assert jsonObj.scheduler_config.labs.count("Test Lab") == 1

def test_lab_add_dupe() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    try:
        Lab.add_lab(jsonObj, "Test Lab")
    except Lab.LabExistsError:
        assert jsonObj.scheduler_config.labs.count("Test Lab") == 1

def test_lab_del() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    Lab.del_lab(jsonObj, "Test Lab")
    assert jsonObj.scheduler_config.labs.count("Test Lab") == 0

def test_lab_del_ne() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Lab.del_lab(jsonObj, "Test Lab")
        assert False
    except Lab.LabMissingError:
        assert True


def test_lab_mod() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    Lab.mod_lab(jsonObj, "Test Lab", "New Lab")
    assert jsonObj.scheduler_config.labs.count("New Lab") == 1

def test_lab_mod_ne() -> None:
    runner = CliRunner()
    obj = {}
    runner.invoke(base_cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Lab.mod_lab(jsonObj, "Test Lab", "New Lab")
        assert False
    except Lab.LabMissingError:
        assert True

