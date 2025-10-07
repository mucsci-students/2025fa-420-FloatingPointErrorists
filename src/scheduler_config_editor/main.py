import sys
from cli.base_cli import cli, apply_signal_handlers

def main() -> None:
    is_cli_mode = False
    for arg in sys.argv[1:]:
        if arg != "-cli":
            print(f"Error: Invalid argument: {arg}")
            sys.exit(1)
        else:
            is_cli_mode = True
    if is_cli_mode:
        sys.argv.remove("-cli")
        apply_signal_handlers()
        cli()
    else:
        print("Not Yet Implemented")

if __name__ == "__main__":
    main()