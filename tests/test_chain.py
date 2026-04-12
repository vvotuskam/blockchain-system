from app.blockchain.chain import SimpleBlockchain


def test_add_and_find_record(tmp_path):
    path = tmp_path / "chain.json"

    bc = SimpleBlockchain(str(path))

    record = {
        "hash": "abc123",
        "signature": "sig",
        "status": "valid"
    }

    bc.add_record(record)

    result = bc.find_by_hash("abc123")

    assert result is not None
    assert result["hash"] == "abc123"


def test_chain_persistence(tmp_path):
    path = tmp_path / "chain.json"

    bc = SimpleBlockchain(str(path))

    bc.add_record({"hash": "x1"})

    bc2 = SimpleBlockchain(str(path))
    result = bc2.find_by_hash("x1")

    assert result is not None
