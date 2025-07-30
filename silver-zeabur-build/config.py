import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./silver.db")
RUST_ANALYZER_PATH = os.getenv("RUST_ANALYZER_PATH", "rust-analyzer")
CARGO_CALL_STACK_PATH = os.getenv("CARGO_CALL_STACK_PATH", "cargo-call-stack")
REPO_CACHE_DIR = os.getenv("REPO_CACHE_DIR", "./repo_cache") 