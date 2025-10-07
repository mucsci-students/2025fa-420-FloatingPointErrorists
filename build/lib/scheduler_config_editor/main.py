import sys
from scheduler_cli.cli.base_cli import cli, apply_signal_handlers
from scheduler_config_editor.view.view import view

def main() -> None:
    apply_signal_handlers()
    if "-cli" in sys.argv:
        sys.argv.remove("-cli")
        apply_signal_handlers()
        cli()
    else:
        view()    

if __name__ == "__main__":
    main()