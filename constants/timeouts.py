from enum import Enum

# ----------------------
# Default Test Timeouts
# ----------------------


class Timeouts(int, Enum):
    SHORT = 2000
    MEDIUM = 5000
    LONG = 10000
    VERY_LONG = 30000
