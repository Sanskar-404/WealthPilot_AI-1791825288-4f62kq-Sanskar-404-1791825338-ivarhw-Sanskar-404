import json, os
from datetime import datetime, timezone

AUDIT_PATH = os.path.join(os.path.dirname(__file__), "audit_log.jsonl")

def log_event(event_type, portfolio_id, payload):
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), "event_type": event_type,
              "portfolio_id": portfolio_id, "payload": payload}
    os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)
    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    return record

def read_events(limit=500):
    if not os.path.exists(AUDIT_PATH):
        return []
    with open(AUDIT_PATH, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    return rows[-limit:]
