# Dummy resolver for demo
# In production, fetch from RustSec API or local DB

def resolve_hash(rustsec_id):
    # Example: return (repo_url, commit_hash, test_hash)
    # TODO: Replace with real RustSec data lookup
    return (
        "https://github.com/rust-lang/example-vuln.git",
        "abcdef1234567890abcdef1234567890abcdef12",
        "testhash1234567890"
    ) 