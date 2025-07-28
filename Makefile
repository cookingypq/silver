.PHONY: help install build run dev clean docker-build docker-run

help: ## 显示帮助信息
	@echo "可用的命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装所有依赖
	@echo "安装 Python 依赖..."
	cd silver && pip install -r requirements.txt
	@echo "安装前端依赖..."
	cd frontend && npm install
	@echo "编译 Rust 工具..."
	cd silver/rust_static && cargo build --release

build: ## 构建项目
	@echo "构建前端..."
	cd frontend && npm run build
	@echo "编译 Rust 工具..."
	cd silver/rust_static && cargo build --release

run: ## 运行生产环境
	@echo "启动后端服务..."
	cd silver && uvicorn main:app --host 0.0.0.0 --port 8000

dev: ## 运行开发环境
	@echo "启动后端开发服务器..."
	cd silver && uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
	@echo "启动前端开发服务器..."
	cd frontend && npm run dev

docker-build: ## 构建 Docker 镜像
	docker build -t silver-app .

docker-run: ## 运行 Docker 容器
	docker run -p 8000:8000 silver-app

docker-compose-up: ## 使用 Docker Compose 启动
	docker-compose up -d

docker-compose-dev: ## 使用 Docker Compose 启动开发环境
	docker-compose --profile dev up -d

clean: ## 清理构建文件
	@echo "清理前端构建文件..."
	rm -rf frontend/dist
	@echo "清理 Rust 构建文件..."
	cd silver/rust_static && cargo clean
	@echo "清理 Python 缓存..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test: ## 运行测试
	@echo "运行前端测试..."
	cd frontend && npm test
	@echo "运行后端测试..."
	cd silver && python -m pytest

lint: ## 代码检查
	@echo "检查前端代码..."
	cd frontend && npm run lint
	@echo "检查 Python 代码..."
	cd silver && flake8 . --max-line-length=88 