from .base_cli import cli, apply_signal_handlers

def main() -> None:
    apply_signal_handlers()
    cli()

if __name__ == "__main__":
    main()