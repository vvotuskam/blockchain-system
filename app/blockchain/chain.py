import json
import os
from datetime import datetime

class SimpleBlockchain:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump([], f)

    def load(self):
        with open(self.path, 'r') as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_record(self, record: dict):
        chain = self.load()
        record["timestamp"] = datetime.utcnow().isoformat()
        chain.append(record)
        self.save(chain)

    def find_by_hash(self, file_hash: str):
        chain = self.load()
        for record in chain:
            if record["hash"] == file_hash:
                return record
        return None