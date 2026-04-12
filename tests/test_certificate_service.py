from app.services.certificate_service import CertificateService
from app.blockchain.chain import SimpleBlockchain

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

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


def test_issue_and_verify(tmp_path):
    chain_file = tmp_path / "chain.json"
    bc = SimpleBlockchain(str(chain_file))

    private_key, public_key = generate_keys()

    service = CertificateService(
        blockchain=bc,
        private_key=private_key,
        public_key=public_key
    )

    file_path = tmp_path / "file.txt"
    file_path.write_text("hello")

    issue_result = service.issue(str(file_path))
    assert issue_result["status"] == "ISSUED"

    verify_result = service.verify(str(file_path))
    assert verify_result["status"] == "VALID"
    assert verify_result["reason"] == "OK"


def test_tampered_file(tmp_path):
    chain_file = tmp_path / "chain.json"
    bc = SimpleBlockchain(str(chain_file))

    private_key, public_key = generate_keys()

    service = CertificateService(
        blockchain=bc,
        private_key=private_key,
        public_key=public_key
    )

    file1 = tmp_path / "file1.txt"
    file1.write_text("hello")

    file2 = tmp_path / "file2.txt"
    file2.write_text("hello MODIFIED")

    service.issue(str(file1))

    result = service.verify(str(file2))

    assert result["status"] == "INVALID"