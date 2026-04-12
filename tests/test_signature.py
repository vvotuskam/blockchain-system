from app.crypto.signature import sign_data, verify_signature
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_bytes, public_bytes


def test_signature_valid():
    private_key, public_key = generate_keys()

    data = b"test-data"
    signature = sign_data(private_key, data)

    assert verify_signature(public_key, signature, data)


def test_signature_invalid_data():
    private_key, public_key = generate_keys()

    data = b"test-data"
    signature = sign_data(private_key, data)

    assert not verify_signature(public_key, signature, b"other-data")