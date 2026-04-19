from app.crypto.signature import sign_data, verify_signature
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return priv_pem, pub_pem


def test_signature_valid():
    priv, pub = generate_keys()

    msg = "test-data"

    sig = sign_data(priv, msg)
    assert verify_signature(pub, msg, sig) is True


def test_signature_invalid():
    priv, pub = generate_keys()

    msg = "test-data"
    sig = sign_data(priv, msg)

    assert verify_signature(pub, "wrong-data", sig) is False