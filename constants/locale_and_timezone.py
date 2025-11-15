from enum import Enum

# -----------------------------
# Locale & Timezone
# -----------------------------


class Locale(Enum):
    EN_US = "en-US"
    EN_GB = "en-GB"
    RO_RO = "en-RO"


class Timezone(Enum):
    UTC = "UTC"
    EET = "Europe/Bucharest"
    PST = "America/Los_Angeles"
