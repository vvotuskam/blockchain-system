from app.crypto.hash_utils import calculate_hash
import tempfile

def test_hash_changes_with_content():
    f1 = tempfile.NamedTemporaryFile(delete=False)
    f1.write(b"hello")
    f1.close()

    f2 = tempfile.NamedTemporaryFile(delete=False)
    f2.write(b"hello world")
    f2.close()

    h1 = calculate_hash(f1.name)
    h2 = calculate_hash(f2.name)

    assert h1 != h2