from config import OPENAI_API_KEY

def llm_call_chain(repo_path, test_hash, context=None):
    # TODO: Replace with real LLM API call
    # Use context (static_chain) as input
    # Example: call OpenAI API
    # response = openai.ChatCompletion.create(...)
    llm_chain = f"LLM call chain for {repo_path}@{test_hash} (context: {context})"
    llm_score = 85  # Dummy confidence
    return llm_chain, llm_score 