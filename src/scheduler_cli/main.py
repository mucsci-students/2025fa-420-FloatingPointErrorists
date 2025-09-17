from .cli import run_shell, apply_signal_handlers

def main() -> None:
    apply_signal_handlers()
    run_shell()

if __name__ == "__main__":
    main()