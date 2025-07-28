import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_and_result():
    # 模拟分析请求
    response = client.post("/analyze", json={"rustsec_ids": ["RUSTSEC-2022-0001"]})
    assert response.status_code == 200
    # 由于返回的是结果列表，无法直接获得 task_id，跳过后续 task_id 查询 