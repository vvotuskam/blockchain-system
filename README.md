# Blockchain Certificate Verification

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

## Generate keys

```bash
mkdir -p keys
openssl genrsa -out keys/private_key.pem 2048
openssl rsa -in keys/private_key.pem -pubout -out keys/public_key.pem
```

## Run

```bash
python main.py issue file.pdf
python main.py verify file.pdf