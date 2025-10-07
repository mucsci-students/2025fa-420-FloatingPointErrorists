import sys
import click
from .base_cli import cli, apply_signal_handlers

def main() -> None:
    if "-cli" in sys.argv:
        sys.argv.remove("-cli")
        apply_signal_handlers()
        cli()
    else:
        print("Not Yet Implemented")

if __name__ == "__main__":
    main()