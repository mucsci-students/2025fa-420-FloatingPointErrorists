import json
from click.testing import CliRunner
from scheduler_cli import cli, run_shell

def test_cli_has_commands():
    assert "load" in cli.commands
    assert "quit" in cli.commands
    assert "show" in cli.commands
    assert "save" in cli.commands

def test_load_config_valid_json(tmp_path):
    runner = CliRunner()
    # Create a temporary JSON file
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"name": "Scheduler"}))
    result = runner.invoke(cli, ["load", str(config)])
    assert result.exit_code == 0
    assert "Configuration loaded" in result.output

def test_load_config_invalid_file():
    runner = CliRunner()
    result = runner.invoke(cli, ["load", "nonexistent.json"])
    # Click should handle this gracefully
    assert result.exit_code != 0
    assert "Path 'nonexistent.json' does not exist." in result.output

def test_load_config_invalid_json(tmp_path):
    runner = CliRunner()
    config = tmp_path / "bad.json"
    config.write_text("{ not: valid json }")
    result = runner.invoke(cli, ["load", str(config)])
    assert result.exit_code != 0
    assert "Invalid JSON" in result.output

def test_show_config(tmp_path):
    file = tmp_path / "show.json"
    file.write_text(json.dumps({"config": {"rooms": ["Roddy 136", "Roddy 140", "Roddy 147"]}}))
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", str(file)], obj=obj)
    result = runner.invoke(cli, ["show"], obj=obj)
    assert 'Rooms:' in result.output
    assert '- Roddy 136' in result.output
    assert '- Roddy 140' in result.output
    assert '- Roddy 147' in result.output

def test_show_config_no_config():
    runner = CliRunner()
    result = runner.invoke(cli, ["show"])
    assert "No configuration loaded." in result.output

def test_save_config(tmp_path):
    file = tmp_path / "save.json"
    file.write_text(json.dumps({"a": 1}))
    runner = CliRunner()
    obj = {}
    runner.invoke(cli, ["load", str(file)], obj=obj)
    result = runner.invoke(cli, ["save"], obj=obj)
    assert "Configuration saved." in result.output
    assert json.loads(file.read_text())["a"] == 1

def test_save_config_no_config():
    runner = CliRunner()
    result = runner.invoke(cli, ["save"], obj={})
    assert "No configuration loaded." in result.output

def test_quit_command_exits():
    runner = CliRunner()
    result = runner.invoke(cli, ["quit"])
    assert result.exit_code == 0  # SystemExit

def test_run_shell_help(monkeypatch, capsys):
    # Provide "help" then "quit" as fake input
    inputs = iter(["help", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_shell()
    out, err = capsys.readouterr()
    assert "Welcome to the Scheduler CLI!" in out
    assert "Usage:" in out  # help text should show