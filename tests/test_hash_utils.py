from app.crypto.hash_utils import calculate_hash


def test_hash_different_files(tmp_path):
    file1 = tmp_path / "a.txt"
    file2 = tmp_path / "b.txt"

    file1.write_text("hello")
    file2.write_text("hello world")

    assert calculate_hash(str(file1)) != calculate_hash(str(file2))


def test_hash_same_file(tmp_path):
    file1 = tmp_path / "a.txt"
    file1.write_text("hello")

    h1 = calculate_hash(str(file1))
    h2 = calculate_hash(str(file1))

    assert h1 == h2