import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def sign(private_key_pem, message: str):
    key = serialization.load_pem_private_key(private_key_pem, None)

    signature = key.sign(
        message.encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    return base64.b64encode(signature).decode()


def verify(public_key_pem, message: str, signature: str):
    key = serialization.load_pem_public_key(public_key_pem)

    try:
        key.verify(
            base64.b64decode(signature),
            message.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False