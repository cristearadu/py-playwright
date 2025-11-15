from enum import Enum, auto

# ----------------------------
# Default CLI Pytest commands
# ----------------------------


class CliConfigCommands(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return f"--{name.lower()}"

    BROWSER = "--run-browser"
    HEADLESS = auto()
