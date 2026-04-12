import argparse
import os
from dotenv import load_dotenv

from app.blockchain.chain import SimpleBlockchain
from app.services.certificate_service import CertificateService


def load_keys():
    with open(os.getenv("PRIVATE_KEY_PATH"), "rb") as f:
        private_key = f.read()
    with open(os.getenv("PUBLIC_KEY_PATH"), "rb") as f:
        public_key = f.read()
    return private_key, public_key


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["issue", "verify"])
    parser.add_argument("file")

    args = parser.parse_args()

    blockchain = SimpleBlockchain(os.getenv("CHAIN_FILE"))
    private_key, public_key = load_keys()

    service = CertificateService(blockchain, private_key, public_key)

    if args.command == "issue":
        result = service.issue(args.file)
        print(result["status"], result["file_hash"])

    elif args.command == "verify":
        result = service.verify(args.file)
        print(result["status"], result.get("reason"))


if __name__ == "__main__":
    main()