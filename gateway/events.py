"""Write gateway events as JSON lines (one event per line)."""
import json
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("logs/events.jsonl")


def log_event(event_type: str, **fields) -> None:
    LOG_FILE.parent.mkdir(exist_ok=True)
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_type,
        **fields,
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")