import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from mlrds import r_hash, MLRDS


def test_r_hash_length():
    result = r_hash("test")
    assert re.fullmatch(r"[0-9a-f]{128}", result)


def test_mlrds_send():
    system = MLRDS()
    payload = "hello"
    result = system.send(payload)
    assert result["payload"].startswith("reflected:")
    assert result["mirror_origin"] == "MirrorA"
    assert result["mirror_target"] == "MirrorB"

