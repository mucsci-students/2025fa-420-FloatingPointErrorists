import json
from click.testing import CliRunner
from scheduler_cli import cli, run_shell

def test_cli_has_commands():
    assert "load-config" in cli.commands
    assert "quit" in cli.commands

def test_load_config_valid_json(tmp_path):
    runner = CliRunner()
    # Create a temporary JSON file
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"name": "Scheduler"}))
    result = runner.invoke(cli, ["load-config", str(config_file)])
    assert result.exit_code == 0
    assert "Configuration loaded:" in result.output
    assert '"name": "Scheduler"' in result.output

def test_load_config_invalid_file():
    runner = CliRunner()
    result = runner.invoke(cli, ["load-config", "nonexistent.json"])
    # Click should handle this gracefully
    assert result.exit_code != 0
    assert "Invalid value for 'PATH'" in result.output

def test_load_config_invalid_json(tmp_path):
    runner = CliRunner()
    config_file = tmp_path / "bad.json"
    config_file.write_text("{ not: valid json }")
    result = runner.invoke(cli, ["load-config", str(config_file)])
    assert result.exit_code != 0
    assert "Error" in result.output or "JSON" in result.output

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