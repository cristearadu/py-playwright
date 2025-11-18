import os
from dotenv import load_dotenv
from dataclasses import dataclass
from constants import Timezone, Locale, DefaultGeolocation

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """
    Global framework settings loaded from the env variables
    All defaults should be explicit and environment-driven
    """

    # Application base URL
    saucedemo_base_url: str = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com/")
    practice_base_url = os.getenv("PRACTICE_BASE_URL", "https://rahulshettyacademy.com/AutomationPractice/")

    # Environment / locale
    timezone: str = os.getenv("DEFAULT_TIMEZONE", Timezone.UTC.value)
    locale: str = os.getenv("DEFAULT_LOCALE", Locale.EN_US)

    # Geolocation
    geo_lat: float = float(os.getenv("DEFAULT_GEO_LAT", DefaultGeolocation.LAT.value))
    geo_lon: float = float(os.getenv("DEFAULT_GEO_LON", DefaultGeolocation.LON.value))

    default_width: int = 1920
    default_height: int = 1080
