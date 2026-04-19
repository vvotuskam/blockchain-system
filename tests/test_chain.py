import tempfile
from app.blockchain.chain import SimpleBlockchain


def test_block_addition():
    file = tempfile.NamedTemporaryFile(delete=False)

    bc = SimpleBlockchain(file.name)

    bc.add_block({"file_hash": "abc"})
    bc.add_block({"file_hash": "def"})

    assert len(bc.get_chain()) == 2


def test_chain_persistence():
    file = tempfile.NamedTemporaryFile(delete=False)

    bc1 = SimpleBlockchain(file.name)
    bc1.add_block({"file_hash": "abc"})

    bc2 = SimpleBlockchain(file.name)

    assert len(bc2.get_chain()) == 1