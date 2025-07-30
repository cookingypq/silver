import os
import subprocess
from config import REPO_CACHE_DIR

def ensure_repo(repo_url, commit_hash):
    os.makedirs(REPO_CACHE_DIR, exist_ok=True)
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(REPO_CACHE_DIR, repo_name)
    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
    subprocess.run(["git", "fetch"], cwd=repo_path, check=True)
    subprocess.run(["git", "checkout", commit_hash], cwd=repo_path, check=True)
    return repo_path

def clone_and_checkout(repo_url, commit_hash):
    # 直接调用 ensure_repo，便于测试
    return ensure_repo(repo_url, commit_hash) 