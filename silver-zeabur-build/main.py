from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
from loguru import logger
from config import DATABASE_URL
from repo_manager import ensure_repo
from hash_resolver import resolve_hash
from static_analyzer import analyze_call_chain
from llm_helper import llm_call_chain
from validator import cross_validate
from exporter import export_results

app = FastAPI(title="Silver RustSec Analyzer API")

# In-memory task/result store for demo (replace with DB in prod)
tasks = {}

class AnalyzeRequest(BaseModel):
    rustsec_ids: List[str]

class AnalyzeResult(BaseModel):
    id: str
    status: str
    confidence: Optional[int]
    call_chain: Optional[str]
    error: Optional[str] = None

@app.post("/analyze", response_model=List[AnalyzeResult])
def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    results = []
    for rid in request.rustsec_ids:
        results.append({"id": rid, "status": "pending", "confidence": None, "call_chain": None, "error": None})
    tasks[task_id] = results
    background_tasks.add_task(run_analysis, task_id, request.rustsec_ids)
    return results

@app.get("/result/{task_id}", response_model=List[AnalyzeResult])
def get_result(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.get("/export/{task_id}")
def export(task_id: str, fmt: str = "json"):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    file_path = export_results(tasks[task_id], fmt)
    return FileResponse(file_path, filename=os.path.basename(file_path))

# --- Analysis Pipeline ---
def run_analysis(task_id, rustsec_ids):
    for i, rid in enumerate(rustsec_ids):
        try:
            repo_url, commit_hash, test_hash = resolve_hash(rid)
            repo_path = ensure_repo(repo_url, commit_hash)
            static_chain = analyze_call_chain(repo_path, test_hash)
            llm_chain, llm_score = llm_call_chain(repo_path, test_hash, context=static_chain)
            final_chain, confidence = cross_validate(static_chain, llm_chain, llm_score)
            tasks[task_id][i].update({
                "status": "done",
                "confidence": confidence,
                "call_chain": final_chain,
            })
        except Exception as e:
            logger.error(f"Analysis failed for {rid}: {e}")
            tasks[task_id][i].update({
                "status": "failed",
                "error": str(e),
            }) 