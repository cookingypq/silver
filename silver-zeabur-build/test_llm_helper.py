from llm_helper import llm_call_chain

def test_llm_call_chain():
    chain, score = llm_call_chain("repo", "hash", context="static")
    assert "repo" in chain
    assert "hash" in chain
    assert isinstance(score, int)
    assert 0 <= score <= 100 