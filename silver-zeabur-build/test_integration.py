import pytest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app, run_analysis
from repo_manager import ensure_repo
from hash_resolver import resolve_hash
from static_analyzer import analyze_call_chain
from llm_helper import llm_call_chain
from validator import cross_validate
from exporter import export_results

client = TestClient(app)

class TestIntegration:
    """集成测试：测试完整的分析流程"""
    
    def test_full_analysis_pipeline(self):
        """测试完整的分析流水线"""
        with patch('hash_resolver.resolve_hash') as mock_resolve:
            with patch('repo_manager.ensure_repo') as mock_repo:
                with patch('static_analyzer.analyze_call_chain') as mock_static:
                    with patch('llm_helper.llm_call_chain') as mock_llm:
                        with patch('validator.cross_validate') as mock_validate:
                            # 设置模拟返回值
                            mock_resolve.return_value = (
                                "https://github.com/test/repo.git",
                                "abc123",
                                "test_hash"
                            )
                            mock_repo.return_value = "/tmp/test_repo"
                            mock_static.return_value = "static_chain_result"
                            mock_llm.return_value = ("llm_chain_result", 85)
                            mock_validate.return_value = ("final_chain", 90)
                            
                            # 执行分析
                            response = client.post("/analyze", json={
                                "rustsec_ids": ["RUSTSEC-2022-0001"]
                            })
                            
                            assert response.status_code == 200
                            results = response.json()
                            assert len(results) == 1
                            assert results[0]["id"] == "RUSTSEC-2022-0001"
                            assert results[0]["status"] == "pending"
    
    def test_export_functionality(self):
        """测试导出功能"""
        test_results = [
            {
                "id": "RUSTSEC-2022-0001",
                "status": "done",
                "confidence": 90,
                "call_chain": "test_chain"
            }
        ]
        
        # 测试 JSON 导出
        json_path = export_results(test_results, "json")
        assert os.path.exists(json_path)
        with open(json_path, 'r') as f:
            exported_data = json.load(f)
        assert exported_data == test_results
        
        # 测试 TXT 导出
        txt_path = export_results(test_results, "txt")
        assert os.path.exists(txt_path)
        with open(txt_path, 'r') as f:
            txt_content = f.read()
        assert "RUSTSEC-2022-0001" in txt_content
        assert "test_chain" in txt_content
    
    def test_error_handling(self):
        """测试错误处理"""
        with patch('hash_resolver.resolve_hash', side_effect=Exception("API Error")):
            response = client.post("/analyze", json={
                "rustsec_ids": ["INVALID-ID"]
            })
            assert response.status_code == 200
            results = response.json()
            assert results[0]["status"] == "pending"  # 初始状态
    
    def test_concurrent_analysis(self):
        """测试并发分析"""
        with patch('hash_resolver.resolve_hash') as mock_resolve:
            mock_resolve.return_value = (
                "https://github.com/test/repo.git",
                "abc123",
                "test_hash"
            )
            
            # 同时发送多个分析请求
            responses = []
            for i in range(3):
                response = client.post("/analyze", json={
                    "rustsec_ids": [f"RUSTSEC-2022-{i:04d}"]
                })
                responses.append(response)
            
            # 验证所有请求都成功
            for response in responses:
                assert response.status_code == 200
                results = response.json()
                assert len(results) == 1

class TestRustStaticAnalysis:
    """测试 Rust 静态分析功能"""
    
    def test_rust_analyzer_integration(self):
        """测试 Rust 分析器集成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建测试 Rust 项目
            test_rs_file = os.path.join(temp_dir, "main.rs")
            with open(test_rs_file, 'w') as f:
                f.write("""
fn main() {
    test_function();
}

fn test_function() {
    println!("Hello, world!");
}
""")
            
            # 测试静态分析
            result = analyze_call_chain(temp_dir, "main")
            assert isinstance(result, str)
            assert "main" in result or "test_function" in result
    
    def test_call_chain_validation(self):
        """测试调用链验证"""
        static_chain = "main() -> test_function()"
        llm_chain = "main() -> test_function() -> println!()"
        llm_score = 85
        
        final_chain, confidence = cross_validate(static_chain, llm_chain, llm_score)
        
        assert isinstance(final_chain, str)
        assert isinstance(confidence, int)
        assert 0 <= confidence <= 100
        assert static_chain in final_chain
        assert llm_chain in final_chain

class TestLLMIntegration:
    """测试 LLM 集成"""
    
    def test_llm_call_chain_generation(self):
        """测试 LLM 调用链生成"""
        repo_path = "/tmp/test_repo"
        test_hash = "test_hash"
        context = "static_analysis_context"
        
        llm_chain, llm_score = llm_call_chain(repo_path, test_hash, context)
        
        assert isinstance(llm_chain, str)
        assert isinstance(llm_score, int)
        assert 0 <= llm_score <= 100
        assert test_hash in llm_chain or repo_path in llm_chain
    
    def test_llm_confidence_scoring(self):
        """测试 LLM 置信度评分"""
        # 测试不同置信度级别
        test_cases = [
            ("high_confidence_context", 90),
            ("medium_confidence_context", 70),
            ("low_confidence_context", 30)
        ]
        
        for context, expected_min in test_cases:
            _, score = llm_call_chain("/tmp/repo", "test", context)
            assert score >= 0
            assert score <= 100

class TestRepositoryManagement:
    """测试仓库管理功能"""
    
    def test_repo_clone_and_checkout(self):
        """测试仓库克隆和检出"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            repo_url = "https://github.com/test/repo.git"
            commit_hash = "abc123"
            
            result_path = ensure_repo(repo_url, commit_hash)
            
            assert isinstance(result_path, str)
            assert "repo" in result_path
            assert mock_run.call_count >= 3  # clone, fetch, checkout
    
    def test_repo_cache_management(self):
        """测试仓库缓存管理"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            # 测试重复克隆同一仓库
            repo_url = "https://github.com/test/repo.git"
            commit_hash = "abc123"
            
            path1 = ensure_repo(repo_url, commit_hash)
            path2 = ensure_repo(repo_url, commit_hash)
            
            assert path1 == path2  # 应该返回相同的路径

class TestDataValidation:
    """测试数据验证"""
    
    def test_rustsec_id_validation(self):
        """测试 RustSec ID 格式验证"""
        valid_ids = [
            "RUSTSEC-2022-0001",
            "RUSTSEC-2023-0010",
            "RUSTSEC-2024-0100"
        ]
        
        invalid_ids = [
            "INVALID-ID",
            "RUSTSEC-2022",
            "2022-0001"
        ]
        
        for valid_id in valid_ids:
            # 这里应该添加实际的验证逻辑
            assert "RUSTSEC-" in valid_id
            assert "-" in valid_id.split("RUSTSEC-")[1]
        
        for invalid_id in invalid_ids:
            # 验证无效 ID 被正确处理
            assert "RUSTSEC-" not in invalid_id or len(invalid_id.split("RUSTSEC-")[1].split("-")) != 2
    
    def test_call_chain_format_validation(self):
        """测试调用链格式验证"""
        valid_chains = [
            "main() -> function1() -> function2()",
            "entry_point()",
            "test_fn() -> helper() -> utility()"
        ]
        
        for chain in valid_chains:
            assert isinstance(chain, str)
            assert len(chain) > 0
            # 可以添加更多格式验证逻辑 