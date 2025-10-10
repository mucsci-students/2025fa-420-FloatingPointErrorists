from pathlib import Path
from click.testing import CliRunner
from scheduler_config_editor import cli, Lab

CONFIG_KEY = "config"
LOAD_COMMAND = "load-config"
#Tests to run: Add new, Try to add duplicate, Delete existing, Delete nonexisting, mod existing, mod non existing

def dummy_path() -> str:
    return str(Path(__file__).parent / "dummy.json")

def test_lab_add():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    assert jsonObj.scheduler_config.labs.count("Test Lab") == 1

def test_lab_add_dupe():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    try:
        Lab.add_lab(jsonObj, "Test Lab")
    except ValueError:
        assert jsonObj.scheduler_config.labs.count("Test Lab") == 1

def test_lab_del():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    Lab.del_lab(jsonObj, "Test Lab")
    assert jsonObj.scheduler_config.labs.count("Test Lab") == 0

def test_lab_del_ne():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Lab.del_lab(jsonObj, "Test Lab")
        assert False
    except ValueError:
        assert True


def test_lab_mod():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    Lab.add_lab(jsonObj, "Test Lab")
    Lab.mod_lab(jsonObj, "Test Lab", "New Lab")
    assert jsonObj.scheduler_config.labs.count("New Lab") == 1

def test_lab_mod_ne():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, dummy_path()], obj=obj)
    jsonObj = obj[CONFIG_KEY]
    try:
        Lab.mod_lab(jsonObj, "Test Lab", "New Lab")
        assert False
    except ValueError:
        assert True

