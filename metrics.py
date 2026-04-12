import os
import time
import shutil
import matplotlib.pyplot as plt

from app.blockchain.chain import SimpleBlockchain
from app.services.certificate_service import CertificateService
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# -----------------------------
# KEY GENERATION
# -----------------------------
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


# -----------------------------
# FILE GENERATOR
# -----------------------------
def generate_file(size_mb: int, base_dir="tmp_metrics"):
    os.makedirs(base_dir, exist_ok=True)

    file_path = os.path.join(base_dir, f"heavy_{size_mb}mb.txt")

    if os.path.exists(file_path):
        return file_path

    print(f"Generating file: {file_path}")

    data = "BLOCKCHAIN_STRESS_TEST_LINE\n" * 1000
    chunks = (size_mb * 1024) // 30

    with open(file_path, "w") as f:
        for _ in range(chunks):
            f.write(data)

    return file_path


# -----------------------------
# CLEANUP
# -----------------------------
def cleanup_tmp(base_dir="tmp_metrics"):
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
        print(f"Cleaned up {base_dir}/")


# -----------------------------
# STRESS TEST
# -----------------------------
def run_stress_test(sizes_mb):
    chain_file = "chain.json"

    bc = SimpleBlockchain(chain_file)

    private_key, public_key = generate_keys()

    service = CertificateService(
        blockchain=bc,
        private_key=private_key,
        public_key=public_key
    )

    issue_times = []
    verify_times = []

    try:
        for size in sizes_mb:
            file_path = generate_file(size)

            # ISSUE
            start = time.time()
            service.issue(file_path)
            issue_time = time.time() - start

            # VERIFY (avg)
            verify_runs = []
            for _ in range(5):
                start = time.time()
                service.verify(file_path)
                verify_runs.append(time.time() - start)

            avg_verify = sum(verify_runs) / len(verify_runs)

            issue_times.append(issue_time)
            verify_times.append(avg_verify)

            print(f"{size}MB -> issue: {issue_time:.4f}s | verify: {avg_verify:.4f}s")

    finally:
        # ALWAYS CLEANUP (even if crash happens)
        cleanup_tmp()

    return issue_times, verify_times


# -----------------------------
# PLOT
# -----------------------------
def plot(sizes, issue_times, verify_times):
    plt.figure()

    plt.plot(sizes, issue_times, marker="o", label="ISSUE time")
    plt.plot(sizes, verify_times, marker="o", label="VERIFY time")

    plt.xlabel("File size (MB)")
    plt.ylabel("Time (seconds)")
    plt.title("Blockchain Stress Test (Size vs Latency)")

    plt.grid(True)
    plt.legend()

    plt.show()


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    sizes_mb = [1, 5, 10, 20, 50]

    issue_times, verify_times = run_stress_test(sizes_mb)

    plot(sizes_mb, issue_times, verify_times)