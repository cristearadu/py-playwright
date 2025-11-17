import os
import logging
from datetime import datetime
from pathlib import Path

ROOT_WORKING_DIRECTORY = Path(__file__).resolve().parents[1]
LOGS_FOLDER = "logs"


def _current_worker_id() -> str:
    # Provided by pytest-xdist; absent in controller process
    return os.environ.get("PYTEST_XDIST_WORKER", "controller")


class _WorkerFilter(logging.Filter):
    """Injects the pytest-xdist worker id into every LogRecord as 'worker'."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.worker = _current_worker_id()
        return True


def init_logger():
    """
    Initialize pytest-compatible logger.
    Creates one log file per test session, shared across workers.
    """
    log_dir = ROOT_WORKING_DIRECTORY / LOGS_FOLDER
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create the main log file (shared across workers)
    if not os.environ.get("PYTEST_LOG_FILE"):
        timestamp = datetime.now().isoformat(timespec="seconds").replace(":", "-")
        log_file = log_dir / f"{timestamp}.log"
        os.environ["PYTEST_LOG_FILE"] = str(log_file)
    else:
        log_file = Path(os.environ["PYTEST_LOG_FILE"])

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # !!! always ensure worker id is attached to records
    root_logger.addFilter(_WorkerFilter())

    if not root_logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(worker)s] %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        file_handler.addFilter(_WorkerFilter())
        root_logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(worker)s] %(message)s")
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)
        console_handler.addFilter(_WorkerFilter())
        root_logger.addHandler(console_handler)

    logger = logging.getLogger("pytest-logger")

    return logger
