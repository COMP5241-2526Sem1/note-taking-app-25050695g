#!/bin/bash

# 部署前测试脚本
echo "🧪 Testing application before deployment..."

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed"
    exit 1
fi

echo "✅ Python3 is installed"

# 检查必需文件
required_files=("src/main.py" "requirements.txt" "vercel.json" "api/index.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file missing: $file"
        exit 1
    fi
done

echo "✅ All required files exist"

# 检查依赖
echo "📦 Checking dependencies..."
pip3 install -q -r requirements.txt

echo "✅ Dependencies installed"

# 运行语法检查
echo "🔍 Checking Python syntax..."
python3 -m py_compile src/main.py
python3 -m py_compile api/index.py

echo "✅ Python syntax is valid"

echo ""
echo "🎉 All checks passed! Ready to deploy to Vercel."
echo ""
echo "Next steps:"
echo "1. Commit your changes: git add . && git commit -m 'Add Vercel configuration'"
echo "2. Push to GitHub: git push origin main"
echo "3. Deploy on Vercel: https://vercel.com/"
