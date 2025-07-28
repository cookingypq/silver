# Silver 项目部署指南

## 🚀 快速开始

### 使用 Docker（推荐）

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd silver

# 2. 设置环境变量
export OPENAI_API_KEY="your-openai-api-key-here"

# 3. 构建并启动
docker-compose up -d

# 4. 访问应用
# 前端: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 使用 Makefile

```bash
# 安装所有依赖
make install

# 开发环境运行
make dev

# 生产环境构建和运行
make build
make run

# 查看所有可用命令
make help
```

## 🔧 环境配置

### 必需的环境变量

```bash
# OpenAI API 密钥
export OPENAI_API_KEY="sk-your-api-key-here"

# 数据库配置（可选）
export DATABASE_URL="sqlite:///./silver.db"
```

### 创建 .env 文件

```bash
# 复制示例文件
cp .env.example .env

# 编辑环境变量
vim .env
```

## 📦 手动部署

### 前端部署

```bash
cd frontend
npm install --legacy-peer-deps
npm run build
# 构建结果在 dist/ 目录
```

### 后端部署

```bash
cd silver
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Rust 工具编译

```bash
cd silver/rust_static
cargo build --release
# 可执行文件在 target/release/rust_static
```

## 🐳 Docker 部署

### 构建镜像

```bash
# 构建所有服务
docker-compose build

# 或构建单个服务
docker build -t silver-app .
```

### 运行容器

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 生产环境配置

```bash
# 使用生产环境配置
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 服务检查

### 健康检查

```bash
# 检查 API 服务
curl http://localhost:8000/docs

# 检查容器状态
docker-compose ps

# 查看服务日志
docker-compose logs silver-app
```

### 端口映射

- **8000**: 主应用端口（API + 前端）
- **8001**: 开发环境端口（可选）

## 🛠️ 故障排除

### 常见问题

1. **Docker 守护进程未运行**
   ```bash
   # macOS
   open -a Docker
   
   # Linux
   sudo systemctl start docker
   ```

2. **端口被占用**
   ```bash
   # 查看端口占用
   lsof -i :8000
   
   # 修改端口
   docker-compose up -d -p 8001:8000
   ```

3. **环境变量未设置**
   ```bash
   # 检查环境变量
   echo $OPENAI_API_KEY
   
   # 设置环境变量
   export OPENAI_API_KEY="your-key"
   ```

4. **构建失败**
   ```bash
   # 清理缓存
   docker-compose build --no-cache
   
   # 清理所有镜像
   docker system prune -a
   ```

### 日志查看

```bash
# 查看实时日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs silver-app

# 进入容器调试
docker-compose exec silver-app bash
```

## 📊 监控和维护

### 性能监控

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
docker system df
```

### 备份和恢复

```bash
# 备份数据
docker-compose exec silver-app tar -czf backup.tar.gz /app/data

# 恢复数据
docker-compose exec silver-app tar -xzf backup.tar.gz
```

## 🔐 安全配置

### 生产环境安全

1. **使用 HTTPS**
   ```bash
   # 配置 SSL 证书
   docker-compose -f docker-compose.ssl.yml up -d
   ```

2. **环境变量安全**
   ```bash
   # 使用 Docker secrets
   echo "your-secret" | docker secret create openai_api_key -
   ```

3. **网络隔离**
   ```bash
   # 创建自定义网络
   docker network create silver-network
   ```

## 📝 更新部署

### 代码更新

```bash
# 拉取最新代码
git pull origin main

# 重新构建
docker-compose build --no-cache

# 重启服务
docker-compose down
docker-compose up -d
```

### 版本管理

```bash
# 标记版本
git tag v1.0.0

# 构建特定版本
docker build -t silver-app:v1.0.0 .
```

## 📞 支持

如果遇到问题，请：

1. 查看日志：`docker-compose logs`
2. 检查配置：确保环境变量正确设置
3. 查看文档：访问 http://localhost:8000/docs
4. 提交 Issue：在项目仓库中报告问题 