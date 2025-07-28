from validator import cross_validate

def test_cross_validate():
    static_chain = "static chain"
    llm_chain = "llm chain"
    llm_score = 80
    final_chain, confidence = cross_validate(static_chain, llm_chain, llm_score)
    assert "static chain" in final_chain
    assert "llm chain" in final_chain
    assert 80 < confidence <= 90 