FROM python:3.11-slim

WORKDIR /app

# install openssl for key generation
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# init script: install deps, copy env, generate keys if missing
RUN echo '#!/bin/sh
set -e

# create .env if not exists
if [ ! -f .env ]; then cp .env.example .env; fi

# generate RSA keys if not exists
mkdir -p keys
if [ ! -f keys/private_key.pem ]; then \
  openssl genrsa -out keys/private_key.pem 2048; \
  openssl rsa -in keys/private_key.pem -pubout -out keys/public_key.pem; \
fi

exec "$@"' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "main.py", "--help"]