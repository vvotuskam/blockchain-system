import logging
import os
import requests
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import uvicorn

from app.blockchain.chain import SimpleBlockchain
from app.services.certificate_service import CertificateService
from app.crypto.node_signature import verify, sign


# -------------------------
# LOAD ENV
# -------------------------
load_dotenv()

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# UI SETUP
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------
# NODE CONFIG
# -------------------------
def get_peers():
    return [p for p in os.getenv("PEERS", "").split(",") if p]


def load_keys():
    return (
        open(os.getenv("PRIVATE_KEY_PATH"), "rb").read(),
        open(os.getenv("PUBLIC_KEY_PATH"), "rb").read()
    )


# -------------------------
# INIT SYSTEM
# -------------------------
blockchain = SimpleBlockchain(os.getenv("CHAIN_FILE"))

priv_key, pub_key = load_keys()
service = CertificateService(blockchain, priv_key, pub_key)


# -------------------------
# ISSUE (broadcast to all nodes)
# -------------------------
@app.post("/issue")
async def issue(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = service.issue(path)
    block = result["block"]

    # blockchain.add_block(block)

    # broadcast to peers
    for peer in get_peers():
        try:
            requests.post(f"{peer}/add_block", json=block, timeout=2)
        except:
            pass

    return result


# -------------------------
# VERIFY (multi-node + quorum + signature check)
# -------------------------
@app.post("/verify")
async def verify_file(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    local = service.verify(path)
    votes = [local["status"]]

    for peer in get_peers():
        try:
            with open(path, "rb") as f:
                files = {"file": (file.filename, f.read())}

            r = requests.post(f"{peer}/verify_block", files=files, timeout=3)
            data = r.json()

            if verify(pub_key, data["status"], data["signature"]):
                votes.append(data["status"])
            else:
                votes.append("INVALID")

        except:
            votes.append("INVALID")

    valid = votes.count("VALID")
    invalid = votes.count("INVALID")
    expired = votes.count("EXPIRED")

    if expired > 0:
        final = "EXPIRED"
    elif invalid > valid:
        final = "INVALID"
    else:
        final = "VALID"

    return {
        "local": local["status"],
        "votes": votes,
        "valid": valid,
        "invalid": invalid,
        "expired": expired,
        "final": final
    }

@app.post("/verify_block")
async def verify_block(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    result = service.verify(path)

    return {
        "status": result["status"],
        "signature": sign(priv_key, result["status"])
    }

# -------------------------
# RECEIVE BLOCK FROM OTHER NODES
# -------------------------
@app.post("/add_block")
async def add_block(block: dict):
    blockchain.add_block(block)
    return {"ok": True}


# -------------------------
# GET CHAIN
# -------------------------
@app.get("/chain")
def get_chain():
    return blockchain.get_chain()


# -------------------------
# RUN SERVER
# -------------------------
def start():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )
    print(get_peers())


if __name__ == "__main__":
    start()