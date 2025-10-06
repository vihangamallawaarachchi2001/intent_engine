import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

class BlockchainLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.ledger_path = self.log_dir / "ledger.jsonl"

    def _last_hash(self) -> str:
        """Get the hash of the last entry, or zeros if no entries exist."""
        if not self.ledger_path.exists():
            return "0" * 64

        file_size = self.ledger_path.stat().st_size
        if file_size == 0:
            return "0" * 64

        try:
            with open(self.ledger_path, "rb") as f:
                # Read all lines and get the last non-empty one
                lines = f.readlines()
                # Filter out empty lines and get the last valid line
                valid_lines = [line for line in lines if line.strip()]
                if not valid_lines:
                    return "0" * 64

                last_line = valid_lines[-1].decode('utf-8').strip()
                if not last_line:
                    return "0" * 64

                last_entry = json.loads(last_line)
                return last_entry.get("hash", "0" * 64)

        except (json.JSONDecodeError, KeyError, OSError):
            return "0" * 64

    def log(self, data: Any):
        timestamp = time.time()
        prev_hash = self._last_hash()
        entry = {
            "timestamp": timestamp,
            "data": data,
            "prev_hash": prev_hash,
        }
        entry_str = json.dumps(entry, separators=(',', ':'))
        current_hash = hashlib.sha256(entry_str.encode()).hexdigest()
        entry["hash"] = current_hash

        with open(self.ledger_path, "a") as f:
            f.write(json.dumps(entry) + "\n")