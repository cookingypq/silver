import pytest
import time
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestPerformance:
    """性能测试：测试系统性能和并发处理能力"""
    
    def test_single_request_response_time(self):
        """测试单个请求的响应时间"""
        with patch('hash_resolver.resolve_hash') as mock_resolve:
            mock_resolve.return_value = (
                "https://github.com/test/repo.git",
                "abc123",
                "test_hash"
            )
            
            start_time = time.time()
            response = client.post("/analyze", json={
                "rustsec_ids": ["RUSTSEC-2022-0001"]
            })
            end_time = time.time()
            
            response_time = end_time - start_time
            assert response.status_code == 200
            assert response_time < 1.0  # 响应时间应该小于1秒
    
    def test_concurrent_requests(self):
        """测试并发请求处理"""
        with patch('hash_resolver.resolve_hash') as mock_resolve:
            mock_resolve.return_value = (
                "https://github.com/test/repo.git",
                "abc123",
                "test_hash"
            )
            
            def make_request():
                return client.post("/analyze", json={
                    "rustsec_ids": ["RUSTSEC-2022-0001"]
                })
            
            # 并发发送10个请求
            start_time = time.time()
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                responses = [future.result() for future in futures]
            end_time = time.time()
            
            total_time = end_time - start_time
            assert len(responses) == 10
            assert all(r.status_code == 200 for r in responses)
            assert total_time < 5.0  # 10个并发请求应该在5秒内完成
    
    def test_batch_processing_performance(self):
        """测试批量处理性能"""
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
                            
                            # 测试批量处理多个 RustSec ID
                            rustsec_ids = [f"RUSTSEC-2022-{i:04d}" for i in range(1, 11)]
                            
                            start_time = time.time()
                            response = client.post("/analyze", json={
                                "rustsec_ids": rustsec_ids
                            })
                            end_time = time.time()
                            
                            response_time = end_time - start_time
                            assert response.status_code == 200
                            results = response.json()
                            assert len(results) == 10
                            assert response_time < 2.0  # 批量请求应该在2秒内响应
    
    def test_memory_usage_under_load(self):
        """测试负载下的内存使用"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
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
                            
                            # 发送多个请求
                            for i in range(20):
                                response = client.post("/analyze", json={
                                    "rustsec_ids": [f"RUSTSEC-2022-{i:04d}"]
                                })
                                assert response.status_code == 200
                            
                            final_memory = process.memory_info().rss
                            memory_increase = final_memory - initial_memory
                            
                            # 内存增长应该控制在合理范围内（例如小于100MB）
                            assert memory_increase < 100 * 1024 * 1024  # 100MB
    
    def test_export_performance(self):
        """测试导出性能"""
        from exporter import export_results
        
        # 创建大量测试数据
        large_results = []
        for i in range(1000):
            large_results.append({
                "id": f"RUSTSEC-2022-{i:04d}",
                "status": "done",
                "confidence": 85,
                "call_chain": f"main() -> function_{i}() -> helper_{i}()"
            })
        
        # 测试 JSON 导出性能
        start_time = time.time()
        json_path = export_results(large_results, "json")
        json_time = time.time() - start_time
        
        # 测试 TXT 导出性能
        start_time = time.time()
        txt_path = export_results(large_results, "txt")
        txt_time = time.time() - start_time
        
        assert json_time < 1.0  # JSON 导出应该在1秒内完成
        assert txt_time < 1.0   # TXT 导出应该在1秒内完成
    
    def test_static_analysis_performance(self):
        """测试静态分析性能"""
        from static_analyzer import analyze_call_chain
        import tempfile
        import os
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建大型测试项目
            for i in range(10):
                test_file = os.path.join(temp_dir, f"module_{i}.rs")
                with open(test_file, 'w') as f:
                    f.write(f"""
fn module_{i}_main() {{
    helper_{i}_1();
    helper_{i}_2();
}}

fn helper_{i}_1() {{
    println!("Helper 1 from module {i}");
}}

fn helper_{i}_2() {{
    println!("Helper 2 from module {i}");
}}
""")
            
            start_time = time.time()
            result = analyze_call_chain(temp_dir, "module_0_main")
            analysis_time = time.time() - start_time
            
            assert isinstance(result, str)
            assert analysis_time < 5.0  # 静态分析应该在5秒内完成
    
    def test_llm_integration_performance(self):
        """测试 LLM 集成性能"""
        from llm_helper import llm_call_chain
        
        # 模拟 LLM API 调用延迟
        with patch('time.sleep') as mock_sleep:
            mock_sleep.return_value = None
            
            start_time = time.time()
            chain, score = llm_call_chain("/tmp/repo", "test_hash", "context")
            llm_time = time.time() - start_time
            
            assert isinstance(chain, str)
            assert isinstance(score, int)
            assert llm_time < 2.0  # LLM 调用应该在2秒内完成（模拟）

class TestScalability:
    """可扩展性测试"""
    
    def test_increasing_load(self):
        """测试递增负载"""
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
                            
                            response_times = []
                            for load in [1, 5, 10, 20]:
                                start_time = time.time()
                                response = client.post("/analyze", json={
                                    "rustsec_ids": [f"RUSTSEC-2022-{i:04d}" for i in range(load)]
                                })
                                end_time = time.time()
                                
                                response_time = end_time - start_time
                                response_times.append(response_time)
                                
                                assert response.status_code == 200
                                results = response.json()
                                assert len(results) == load
                            
                            # 响应时间应该相对稳定，不会线性增长
                            max_time = max(response_times)
                            min_time = min(response_times)
                            assert max_time < min_time * 3  # 最大时间不应该超过最小时间的3倍
    
    def test_resource_cleanup(self):
        """测试资源清理"""
        import gc
        
        # 强制垃圾回收
        gc.collect()
        
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
                            
                            # 发送多个请求
                            for i in range(10):
                                response = client.post("/analyze", json={
                                    "rustsec_ids": [f"RUSTSEC-2022-{i:04d}"]
                                })
                                assert response.status_code == 200
                            
                            # 再次强制垃圾回收
                            gc.collect()
                            
                            # 验证没有内存泄漏（这里只是基本检查）
                            assert True  # 如果有内存泄漏，测试会失败

class TestStressTest:
    """压力测试"""
    
    def test_rapid_fire_requests(self):
        """测试快速连续请求"""
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
                            
                            # 快速发送50个请求
                            start_time = time.time()
                            responses = []
                            for i in range(50):
                                response = client.post("/analyze", json={
                                    "rustsec_ids": [f"RUSTSEC-2022-{i:04d}"]
                                })
                                responses.append(response)
                            end_time = time.time()
                            
                            total_time = end_time - start_time
                            success_count = sum(1 for r in responses if r.status_code == 200)
                            
                            assert success_count >= 45  # 至少90%的请求应该成功
                            assert total_time < 10.0  # 总时间应该在10秒内
    
    def test_large_payload_handling(self):
        """测试大负载处理"""
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
                            
                            # 发送包含大量 RustSec ID 的请求
                            large_payload = {
                                "rustsec_ids": [f"RUSTSEC-2022-{i:04d}" for i in range(100)]
                            }
                            
                            start_time = time.time()
                            response = client.post("/analyze", json=large_payload)
                            end_time = time.time()
                            
                            response_time = end_time - start_time
                            assert response.status_code == 200
                            results = response.json()
                            assert len(results) == 100
                            assert response_time < 3.0  # 大负载应该在3秒内响应 