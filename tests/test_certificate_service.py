import tempfile
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from app.blockchain.chain import SimpleBlockchain
from app.services.certificate_service import CertificateService


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


def test_issue_and_verify():
    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(b"valid document")
    file.close()

    chain_file = tempfile.NamedTemporaryFile(delete=False)

    bc = SimpleBlockchain(chain_file.name)

    priv, pub = generate_keys()

    service = CertificateService(bc, priv, pub)

    result = service.issue(file.name)

    assert result["status"] == "ISSUED"


def test_verify_valid():
    file = tempfile.NamedTemporaryFile(delete=False)
    file.write(b"doc")
    file.close()

    chain_file = tempfile.NamedTemporaryFile(delete=False)

    bc = SimpleBlockchain(chain_file.name)

    priv, pub = generate_keys()

    service = CertificateService(bc, priv, pub)

    service.issue(file.name)

    result = service.verify(file.name)

    assert result["status"] == "VALID"


def test_verify_invalid():
    file1 = tempfile.NamedTemporaryFile(delete=False)
    file1.write(b"doc1")
    file1.close()

    file2 = tempfile.NamedTemporaryFile(delete=False)
    file2.write(b"doc2")
    file2.close()

    chain_file = tempfile.NamedTemporaryFile(delete=False)

    bc = SimpleBlockchain(chain_file.name)

    priv, pub = generate_keys()

    service = CertificateService(bc, priv, pub)

    service.issue(file1.name)

    result = service.verify(file2.name)

    assert result["status"] == "INVALID"