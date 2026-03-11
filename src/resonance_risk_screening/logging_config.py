from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JsonlFileHandler(logging.Handler):
    def __init__(self, path: Path) -> None:
        super().__init__()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path

    def emit(self, record: logging.LogRecord) -> None:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        payload.update(getattr(record, "extra_payload", {}))
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")


def build_logger(log_dir: Path) -> logging.Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("resonance_risk_screening")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    text_handler = logging.FileHandler(log_dir / "run.log", encoding="utf-8")
    text_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    jsonl_handler = JsonlFileHandler(log_dir / "run.jsonl")

    logger.addHandler(text_handler)
    logger.addHandler(jsonl_handler)
    return logger
