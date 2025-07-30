#!/bin/bash

# Zeabur 部署构建脚本
set -e

echo "🚀 开始构建 Silver 项目..."

# 创建构建目录
BUILD_DIR="silver-zeabur-build"
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR

echo "📦 复制 Python 后端文件..."
cp -r silver/* $BUILD_DIR/

echo "🔧 复制配置文件..."
cp zeabur.toml $BUILD_DIR/
cp README.md $BUILD_DIR/

echo "📝 创建启动脚本..."
cat > $BUILD_DIR/start.sh << 'EOF'
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
EOF

chmod +x $BUILD_DIR/start.sh

echo "📋 创建 .nixpacks 配置..."
cat > $BUILD_DIR/.nixpacks << 'EOF'
[phases.setup]
nixPkgs = ["python311", "nodejs_20", "rustc", "cargo"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "./start.sh"
EOF

echo "📦 创建部署包..."
cd $BUILD_DIR
zip -r ../silver-zeabur-v0.0.2.zip .
cd ..

echo "✅ 构建完成！"
echo "📁 部署包: silver-zeabur-v1.0.0.zip"
echo "📋 下一步: 将 zip 文件上传到 Zeabur" 