import click, json, shlex

@click.group()
def cli():
    """Scheduler CLI — interactive shell."""
    pass

@cli.command("load-config")
@click.argument("path", type=click.Path(exists=True))
def load_config(path):
    """Load a JSON configuration file."""
    try:
        with open(path) as config_file:
            config = json.load(config_file)
            click.echo("Configuration loaded:")
            click.echo(json.dumps(config, indent=2))
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")

@cli.command("quit")
def quit_program():
    """Exit the program."""
    raise SystemExit

def run_shell():
    click.echo("Welcome to the Scheduler CLI!")
    click.echo("Type 'help' to see available commands, 'quit' to exit.\n")
    while True:
        try:
            # prompt user
            raw = input("scheduler> ").strip()
            if not raw:
                continue
            # allow "help" to show commands
            if raw == "help":
                click.echo(cli.get_help(click.Context(cli)))
                continue
            # parse input into args list
            args = shlex.split(raw)
            # invoke click with parsed args
            cli.main(args=args, prog_name="scheduler", standalone_mode=False)
        except SystemExit:
            break
        except Exception as e:
            click.echo(f"Error: {e}")
