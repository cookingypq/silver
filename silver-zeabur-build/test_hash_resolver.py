import pytest
from hash_resolver import resolve_hash

def test_resolve_hash():
    url, commit, test = resolve_hash("RUSTSEC-2022-0001")
    assert url == "https://github.com/rust-lang/example-vuln.git"
    assert commit == "abcdef1234567890abcdef1234567890abcdef12"
    assert test == "testhash1234567890" 