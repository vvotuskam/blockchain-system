#!/bin/bash
set -e

echo "============================"
echo "Setting up project..."
echo "============================"

# 1. Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt


# 2. Create .env if not exists
echo "Setting up .env..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env created"
else
  echo ".env already exists"
fi


# 3. Create keys directory
echo "Generating RSA keys..."
mkdir -p keys

if [ ! -f keys/private_key.pem ]; then
  openssl genrsa -out keys/private_key.pem 2048
  openssl rsa -in keys/private_key.pem -pubout -out keys/public_key.pem
  echo "Keys generated"
else
  echo "Keys already exist"
fi


# 4. Create blockchain file if not exists
echo "Initializing blockchain storage..."
if [ ! -f chain.json ]; then
  echo "[]" > chain.json
  echo "chain.json created"
fi

# 5. ISSUE certificate (valid file)
echo "ISSUING CERTIFICATE (valid.pdf)"
python main.py issue files/valid.pdf


# 6. VERIFY valid case
echo "VERIFY (should be VALID)"
python main.py verify files/valid.pdf


# 7. VERIFY tampered file
echo "VERIFY (should be INVALID)"
python main.py verify files/invalid.pdf


echo "DONE"