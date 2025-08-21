import logging
from logging.handlers import TimedRotatingFileHandler
import json
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "msg": record.getMessage(),
            "name": record.name,
            "request_id": getattr(record, "request_id", None)
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)

def configure_logging(level: str = "INFO"):
    root = logging.getLogger()
    root.setLevel(level)

    fh = TimedRotatingFileHandler(LOG_FILE, when="midnight", backupCount=7, encoding="utf-8")
    fh.setFormatter(JSONFormatter())
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setFormatter(JSONFormatter())
    ch.setLevel(level)

    root.handlers = [fh, ch]

configure_logging()
logger = logging.getLogger(__name__)
