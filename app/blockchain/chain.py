import json
import os


class SimpleBlockchain:
    def __init__(self, path):
        self.path = path
        self.chain = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return []

        try:
            with open(self.path, "r") as f:
                content = f.read().strip()

                if not content:
                    return []

                return json.loads(content)

        except json.JSONDecodeError:
            return []

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.chain, f, indent=2)

    def add_block(self, block):
        self.chain.append(block)
        self.save()

    def get_chain(self):
        return self.chain