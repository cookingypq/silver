#!/bin/bash
set -e

echo "🔧 检查环境变量..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ 错误: OPENAI_API_KEY 环境变量未设置"
    exit 1
fi

echo "🐍 检查 Python 环境..."
python --version

echo "📦 安装依赖..."
pip install -r requirements.txt

echo "🚀 启动应用..."
exec python -m uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
