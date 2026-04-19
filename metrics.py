import time
import requests
import matplotlib.pyplot as plt
import tempfile
import os
import shutil

NODES = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
]


def create_file(size_kb: int):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(os.urandom(size_kb * 1024))
    f.close()
    return f.name


def issue_file(node, file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        start = time.time()
        requests.post(f"{node}/issue", files=files)
        return time.time() - start


def verify_file(node, file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        start = time.time()
        requests.post(f"{node}/verify", files=files)
        return time.time() - start


def run_stress_test():
    sizes = [1, 100, 1024, 1024 * 10, 1024 * 20, 1024 * 50, 1024 * 100, 1024 * 200, 1024 * 500, 1024 * 1000]  # KB
    issue_times = []
    verify_times = []

    for size in sizes:
        file_path = create_file(size)

        node = NODES[0]

        it = issue_file(node, file_path)
        vt = verify_file(node, file_path)

        issue_times.append(it)
        verify_times.append(vt)

        os.remove(file_path)

        print(f"Size={size}KB | issue={it:.3f}s | verify={vt:.3f}s")

    return sizes, issue_times, verify_times

def format_size(kb):
    if kb >= 1024 * 1024:
        return f"{kb / (1024 * 1024):.2f} GB"
    elif kb >= 1024:
        return f"{kb / 1024:.2f} MB"
    else:
        return f"{kb:.0f} KB"


def plot(sizes, issue_times, verify_times):
    labels = [format_size(s) for s in sizes]

    plt.figure(figsize=(10, 6))

    plt.plot(labels, issue_times, marker="o", label="Issue time")
    plt.plot(labels, verify_times, marker="o", label="Verify time")

    plt.xlabel("File size")
    plt.ylabel("Time (s)")
    plt.title("Blockchain Network Performance (Multi-node)")

    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

def cleanup_uploads():
    uploads_dir = "uploads"

    if os.path.exists(uploads_dir):
        shutil.rmtree(uploads_dir)
        print("uploads/ cleaned after metrics run")


if __name__ == "__main__":
    try:
        sizes, issue_t, verify_t = run_stress_test()
        plot(sizes, issue_t, verify_t)
    finally:
        cleanup_uploads()