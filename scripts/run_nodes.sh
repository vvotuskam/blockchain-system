#!/bin/bash

echo "======================================"
echo " Initializing Blockchain Network"
echo "======================================"

# -------------------------------
# 1. CREATE ENV IF NOT EXISTS
# -------------------------------
if [ ! -f .env ]; then
  echo "Creating .env..."
  cp .env.example .env
fi

# -------------------------------
# 2. CREATE KEYS IF NOT EXISTS
# -------------------------------
mkdir -p keys

if [ ! -f keys/private_key.pem ] || [ ! -f keys/public_key.pem ]; then
  echo "Generating RSA keys..."

  openssl genrsa -out keys/private_key.pem 2048
  openssl rsa -in keys/private_key.pem -pubout -out keys/public_key.pem
fi

# -------------------------------
# 3. CLEAN OLD CHAINS
# -------------------------------
echo "Cleaning old blockchain state..."
rm -f chain.*.json

# -------------------------------
# 4. CREATE EMPTY CHAINS FOR NODES
# -------------------------------
echo "Initializing node chains..."

echo "[]" > chain.8000.json
echo "[]" > chain.8001.json
echo "[]" > chain.8002.json

# -------------------------------
# 5. START NODES
# -------------------------------

echo "Starting Node 1..."
PORT=8000 \
PEERS=http://127.0.0.1:8001,http://127.0.0.1:8002 \
PYTHONPATH=. \
CHAIN_FILE=chain.8000.json \
python -m app.api.main > node1.log 2>&1 &
NODE1=$!

echo "Starting Node 2..."
PORT=8001 \
PEERS=http://127.0.0.1:8000,http://127.0.0.1:8002 \
PYTHONPATH=. \
CHAIN_FILE=chain.8001.json \
python -m app.api.main > node2.log 2>&1 &
NODE2=$!

echo "Starting Node 3..."
PORT=8002 \
PEERS=http://127.0.0.1:8000,http://127.0.0.1:8001 \
PYTHONPATH=. \
CHAIN_FILE=chain.8002.json \
python -m app.api.main > node3.log 2>&1 &
NODE3=$!

echo "======================================"
echo " Network is running:"
echo " Node1 -> http://127.0.0.1:8000"
echo " Node2 -> http://127.0.0.1:8001"
echo " Node3 -> http://127.0.0.1:8002"
echo "======================================"

wait $NODE1 $NODE2 $NODE3