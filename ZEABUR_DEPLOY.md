# 🚀 Zeabur 部署指南

## 📦 部署步骤

### 1. 下载 Release
- 下载 `silver-v1.0.0.zip` 文件
- 解压到本地目录

### 2. 上传到 Zeabur
1. 登录 [Zeabur](https://zeabur.com)
2. 点击 "New Project"
3. 选择 "Upload Code"
4. 拖拽 `silver-v1.0.0.zip` 文件到上传区域
5. 等待上传完成

### 3. 配置环境变量
在 Zeabur 项目设置中添加以下环境变量：

```bash
# 必需
OPENAI_API_KEY=your-openai-api-key-here

# 可选
DATABASE_URL=sqlite:///./silver.db
DEBUG=false
LOG_LEVEL=INFO
```

### 4. 部署配置
Zeabur 会自动识别以下配置：
- **构建器**: Nixpacks
- **启动命令**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **端口**: 自动分配

### 5. 启动部署
点击 "Deploy" 按钮开始部署

## 🔧 配置说明

### zeabur.toml 配置
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"

[env]
OPENAI_API_KEY = ""
DATABASE_URL = "sqlite:///./silver.db"
```

### 自动检测的技术栈
- **Python**: 3.11+
- **Node.js**: 20+
- **Rust**: 1.75+
- **FastAPI**: Web 框架
- **React**: 前端框架

## 🌐 访问应用

部署完成后，Zeabur 会提供一个域名，例如：
- `https://your-project.zeabur.app`
- `https://silver-xxxx.zeabur.app`

## 📊 监控和日志

### 查看日志
1. 在 Zeabur 控制台点击项目
2. 进入 "Logs" 标签页
3. 查看实时日志

### 性能监控
- CPU 使用率
- 内存使用情况
- 网络流量
- 响应时间

## 🛠️ 故障排除

### 常见问题

1. **构建失败**
   - 检查环境变量是否正确设置
   - 查看构建日志中的错误信息
   - 确保所有依赖都已正确安装

2. **启动失败**
   - 检查 `OPENAI_API_KEY` 是否有效
   - 查看启动日志
   - 确认端口配置正确

3. **依赖问题**
   - 检查 Python 版本兼容性
   - 确认 Node.js 版本支持
   - 验证 Rust 工具链

### 日志分析
```bash
# 常见错误模式
ERROR: OpenAI API key not found
ERROR: Port already in use
ERROR: Module not found
```

## 🔄 更新部署

### 代码更新
1. 修改代码并提交
2. 创建新的 release
3. 重新上传到 Zeabur
4. 触发重新部署

### 环境变量更新
1. 在 Zeabur 控制台修改环境变量
2. 重新部署项目
3. 验证配置生效

## 📈 性能优化

### 推荐配置
- **内存**: 512MB+
- **CPU**: 0.5 vCPU+
- **存储**: 1GB+

### 优化建议
- 使用 CDN 加速静态资源
- 启用缓存策略
- 监控资源使用情况

## 🔐 安全配置

### 环境变量安全
- 不要在代码中硬编码敏感信息
- 使用 Zeabur 的环境变量功能
- 定期轮换 API 密钥

### 网络安全
- 启用 HTTPS
- 配置 CORS 策略
- 限制 API 访问频率

## 📞 支持

如果遇到问题：
1. 查看 Zeabur 官方文档
2. 检查项目日志
3. 联系技术支持

---

**注意**: 确保在部署前设置正确的 `OPENAI_API_KEY` 环境变量。 