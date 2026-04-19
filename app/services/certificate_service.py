import time
from app.crypto.hash_utils import calculate_hash
from app.crypto.signature import sign_data


class CertificateService:
    def __init__(self, blockchain, private_key, public_key):
        self.blockchain = blockchain
        self.private_key = private_key
        self.public_key = public_key

    def issue(self, file_path):
        file_hash = calculate_hash(file_path)

        issue_ts = int(time.time())
        expire_ts = issue_ts + 60 * 2  # 2 min

        signature = sign_data(self.private_key, file_hash)

        block = {
            "file_hash": file_hash,
            "status": "VALID",
            "issue_timestamp": issue_ts,
            "expire_timestamp": expire_ts,
            "signature": signature
        }

        self.blockchain.add_block(block)

        return {
            "status": "ISSUED",
            "hash": file_hash,
            "block": block
        }

    def verify(self, file_path):
        file_hash = calculate_hash(file_path)
        now = int(time.time())

        for block in self.blockchain.get_chain():
            if block["file_hash"] == file_hash:

                if now > block["expire_timestamp"]:
                    return {
                        "status": "EXPIRED"
                    }

                return {
                    "status": "VALID"
                }

        return {
            "status": "INVALID"
        }