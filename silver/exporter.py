import json
import tempfile

def export_results(results, fmt="json"):
    fd, path = tempfile.mkstemp(suffix=f".{fmt}")
    with open(path, "w", encoding="utf-8") as f:
        if fmt == "json":
            json.dump(results, f, indent=2)
        else:
            for r in results:
                f.write(f"{r['id']}\t{r['status']}\tConfidence: {r.get('confidence', '-')}")
                f.write(f"\n{r.get('call_chain', '')}\n---\n")
    return path

def save(final_chain, confidence):
    # 简单保存逻辑，实际可扩展
    with open("/tmp/silver_test_save.txt", "w", encoding="utf-8") as f:
        f.write(f"{final_chain}\nConfidence: {confidence}\n") 