import pytest
from exporter import save
import os

def test_save():
    path = "/tmp/silver_test_save.txt"
    if os.path.exists(path):
        os.remove(path)
    save("chain", 99)
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "chain" in content
    assert "99" in content 