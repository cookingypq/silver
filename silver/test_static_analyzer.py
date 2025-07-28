from static_analyzer import analyze_call_chain

def test_analyze_call_chain():
    result = analyze_call_chain("repo", "hash")
    assert "repo" in result
    assert "hash" in result 