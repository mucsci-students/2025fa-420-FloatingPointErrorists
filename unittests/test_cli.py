import os
from click.testing import CliRunner
from scheduler_config_editor import cli

DUMMY_JSON = os.path.join(os.path.dirname(__file__), "dummy.json")
LOAD_COMMAND = "load-config"

def test_load_config_valid_json():
    runner = CliRunner()
    result = runner.invoke(cli, [LOAD_COMMAND, DUMMY_JSON])
    assert result.exit_code == 0
    assert "Configuration loaded" in result.output

def test_load_config_new_file():
    runner = CliRunner()
    test_file = "nonexistent"
    try:
        result = runner.invoke(cli, [LOAD_COMMAND, test_file])
        assert result.exit_code == 0
        assert "Configuration loaded" in result.output
    finally:
        if os.path.exists(f"configs/{test_file}.json"):
            os.remove(f"configs/{test_file}.json")

def test_load_config_invalid_json(tmp_path):
    runner = CliRunner()
    config = tmp_path / "bad.json"
    config.write_text("{ not: valid json }")
    result = runner.invoke(cli, [LOAD_COMMAND, str(config)])
    assert result.exit_code != 0
    assert "Invalid JSON" in result.output

def test_show_config():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, DUMMY_JSON], obj=obj)
    result = runner.invoke(cli, ["show"], obj=obj)
    assert 'Rooms:' in result.output
    assert '- Roddy 136' in result.output
    assert '- Roddy 140' in result.output
    assert '- Roddy 147' in result.output

def test_show_config_no_config():
    runner = CliRunner()
    result = runner.invoke(cli, ["show"])
    assert "No configuration loaded." in result.output

def test_save_config():
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, [LOAD_COMMAND, DUMMY_JSON], obj=obj)
    result = runner.invoke(cli, ["save"], obj=obj)
    assert "Configuration saved." in result.output

def test_save_config_no_config():
    runner = CliRunner()
    result = runner.invoke(cli, ["save"], obj={})
    assert "No configuration loaded." in result.output