import base64
import time
from app.crypto.hash_utils import calculate_hash
from app.crypto.signature import sign_data, verify_signature

class CertificateService:
    def __init__(self, blockchain, private_key, public_key):
        self.blockchain = blockchain
        self.private_key = private_key
        self.public_key = public_key

    def issue(self, file_path: str):
        file_hash = calculate_hash(file_path)
        signature = sign_data(self.private_key, file_hash.encode())

        record = {
            "hash": file_hash,
            "signature": base64.b64encode(signature).decode(),
            "status": "valid",
            "issued_at": time.time(),
            "expires_at": time.time() + 60 * 60 * 24  # 1 day
        }

        self.blockchain.add_record(record)
        print("Certificate issued")

    def verify(self, file_path: str):
        file_hash = calculate_hash(file_path)
        record = self.blockchain.find_by_hash(file_hash)

        if not record:
            print("INVALID: Not found")
            return

        signature = base64.b64decode(record["signature"])

        if not verify_signature(self.public_key, signature, file_hash.encode()):
            print("INVALID: Signature")
            return

        if record["status"] != "valid":
            print("INVALID: Revoked")
            return

        if time.time() > record["expires_at"]:
            print("INVALID: Expired")
            return

        print("VALID")
