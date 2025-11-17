from enum import Enum


class SauceDemoUsers(str, Enum):
    STANDARD = "standard_user"
    LOCKED = "locked_out_user"
    PROBLEM = "problem_user"
    PERFORMANCE = "performance_glitch_user"
    ERROR = "error_user"
    VISUAL = "visual_user"

    PASSWORD = "secret_sauce"
