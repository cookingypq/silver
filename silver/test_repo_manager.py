import pytest
from repo_manager import clone_and_checkout

def test_clone_and_checkout(monkeypatch):
    def fake_ensure_repo(url, commit):
        return "/tmp/repo"
    monkeypatch.setattr("repo_manager.ensure_repo", fake_ensure_repo)
    path = clone_and_checkout("url", "commit")
    assert path == "/tmp/repo" 