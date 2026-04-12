# Blockchain Certificate Verification
This project is a simplified blockchain-based certificate verification system.
It stores only hashes and metadata on-chain, while original documents are stored off-chain.

---

## Run project

The project can be started using a single script:

```bash
chmod +x ./scripts/run.sh
./scripts/run.sh
```

This script will:
- install dependencies
- generate RSA keys
- initialize blockchain storage
- create test files
- run issue and verify flows

---

## Run manually

Issue certificate:
```bash
python main.py issue files/valid.pdf
```

Verify certificate:
```bash
python main.py verify files/valid.pdf
```

---

## Run tests

Run all tests using pytest:

```bash
pytest -v
```

---

## Project structure

- app/ - core logic (crypto, blockchain, services)
- tests/ - unit tests
- chain.json - local blockchain storage
- run.sh - automatic project run script

---

## Notes

- Only hashes and metadata are stored in blockchain
- Documents are stored off-chain
- Keys are generated locally for testing purposes