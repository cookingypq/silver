# 多阶段构建 Dockerfile
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --legacy-peer-deps

COPY frontend/ ./
RUN npm run build

# Rust 构建阶段
FROM rust:1.75-alpine AS rust-builder

# 安装必要的构建依赖
RUN apk add --no-cache musl-dev

WORKDIR /app/rust_static
COPY silver/rust_static/ ./
RUN cargo build --release

# Python 后端阶段
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制 Python 依赖
COPY silver/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY silver/ ./

# 复制编译好的 Rust 可执行文件
COPY --from=rust-builder /app/rust_static/target/release/rust_static ./rust_static/

# 复制前端构建文件
COPY --from=frontend-builder /app/frontend/dist ./static

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 