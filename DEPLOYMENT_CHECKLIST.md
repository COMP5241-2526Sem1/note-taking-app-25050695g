# Vercel 部署清单

## ✅ 已完成的修改

### 1. 创建的新文件
- ✅ `vercel.json` - Vercel 配置文件
- ✅ `api/index.py` - Vercel serverless 函数入口
- ✅ `.vercelignore` - 部署时忽略的文件
- ✅ `runtime.txt` - 指定 Python 版本
- ✅ `VERCEL_DEPLOYMENT.md` - 详细部署指南
- ✅ `test-before-deploy.sh` - 部署前测试脚本
- ✅ `DEPLOYMENT_CHECKLIST.md` - 本文件

### 2. 修改的文件
- ✅ `src/main.py` - 添加了 Vercel 环境支持，支持内存数据库和外部数据库
- ✅ `README.md` - 添加了 Vercel 部署说明

### 3. 配置说明

#### vercel.json
```json
{
  "version": 2,
  "builds": [{"src": "api/index.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "api/index.py"}],
  "env": {"VERCEL": "1"}
}
```

#### api/index.py
```python
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.main import app
app = app
```

#### 数据库配置 (src/main.py)
- 支持环境变量 `DATABASE_URL` 用于外部数据库
- Vercel 环境下默认使用内存数据库
- 本地开发使用 SQLite 文件数据库

## 📋 部署前检查

运行测试脚本：
```bash
./test-before-deploy.sh
```

或手动检查：
- [ ] Python 语法无错误
- [ ] 所有依赖已列在 requirements.txt
- [ ] vercel.json 配置正确
- [ ] api/index.py 文件存在
- [ ] 本地测试运行正常

## 🚀 部署步骤

### 选项 A：通过 GitHub + Vercel（推荐）

1. **提交代码到 Git**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **在 Vercel 上导入项目**
   - 访问 https://vercel.com/
   - 使用 GitHub 登录
   - 点击 "Add New..." → "Project"
   - 选择仓库 `note-taking-app-updated-xxwtiancai`
   - 点击 "Import"

3. **配置项目（使用默认设置）**
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: 留空
   - Output Directory: 留空
   - Install Command: `pip install -r requirements.txt`

4. **点击 Deploy**

### 选项 B：通过 Vercel CLI

1. **安装 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **登录**
   ```bash
   vercel login
   ```

3. **部署**
   ```bash
   cd /Users/xiongweixiao/Desktop/polyu-msc/COMP5241/lab2/note-taking-app-updated-xxwtiancai
   vercel
   ```

4. **生产部署**
   ```bash
   vercel --prod
   ```

## ⚙️ 可选：配置外部数据库

### 为什么需要外部数据库？
- Vercel 是无服务器环境，内存数据会在函数重启后丢失
- 生产环境建议使用持久化数据库

### 推荐的免费数据库服务

#### 1. Neon (PostgreSQL) - 推荐
```bash
# 1. 注册：https://neon.tech
# 2. 创建项目
# 3. 复制连接字符串
# 4. 在 Vercel 添加环境变量：
#    Name: DATABASE_URL
#    Value: postgresql://user:password@host/database
```

#### 2. PlanetScale (MySQL)
```bash
# 1. 注册：https://planetscale.com
# 2. 创建数据库
# 3. 复制连接字符串
# 4. 添加到 Vercel 环境变量
```

#### 3. Supabase (PostgreSQL)
```bash
# 1. 注册：https://supabase.com
# 2. 创建项目
# 3. 在 Database Settings 获取连接字符串
# 4. 添加到 Vercel 环境变量
```

### 在 Vercel 添加环境变量

1. 进入项目设置：https://vercel.com/your-username/your-project/settings
2. 点击 "Environment Variables"
3. 添加变量：
   - **Name**: `DATABASE_URL`
   - **Value**: 你的数据库连接字符串
   - **Environment**: Production, Preview, Development (全选)
4. 点击 "Save"
5. 重新部署项目

### 修改数据库模型（如果使用 PostgreSQL）

如果使用 PostgreSQL，可能需要安装额外依赖：

1. 更新 `requirements.txt`：
   ```bash
   echo "psycopg2-binary==2.9.9" >> requirements.txt
   ```

2. 提交并重新部署：
   ```bash
   git add requirements.txt
   git commit -m "Add PostgreSQL support"
   git push origin main
   ```

## 🧪 测试部署

部署成功后：

1. 访问 Vercel 提供的 URL（例如：`https://your-project.vercel.app`）
2. 测试功能：
   - [ ] 首页加载正常
   - [ ] 可以创建笔记
   - [ ] 可以编辑笔记
   - [ ] 可以删除笔记
   - [ ] 搜索功能正常
   - [ ] 刷新页面后数据保持（如果使用外部数据库）

## 🔧 故障排除

### 部署失败
1. 查看 Vercel 部署日志
2. 检查 Python 版本是否兼容
3. 验证 requirements.txt 中的依赖

### 应用无法访问
1. 检查 vercel.json 路由配置
2. 验证 api/index.py 是否正确导入 app

### 数据库连接错误
1. 验证 DATABASE_URL 环境变量
2. 检查数据库服务是否运行
3. 确认连接字符串格式正确

### API 请求失败
1. 检查浏览器控制台错误
2. 验证 CORS 配置
3. 查看 Vercel 函数日志

## 📊 监控和日志

### 查看日志
1. 访问 Vercel Dashboard
2. 选择你的项目
3. 点击 "Logs" 标签
4. 查看实时日志和错误

### 性能监控
- Vercel 自动提供性能指标
- 在项目的 "Analytics" 标签查看

## 🔄 更新应用

### 通过 GitHub（自动）
```bash
# 修改代码
git add .
git commit -m "Update feature"
git push origin main
# Vercel 自动检测并部署
```

### 通过 CLI（手动）
```bash
vercel --prod
```

## 📚 相关资源

- [Vercel 部署指南](VERCEL_DEPLOYMENT.md) - 详细部署说明
- [Vercel 官方文档](https://vercel.com/docs)
- [Vercel Python 运行时](https://vercel.com/docs/functions/runtimes/python)
- [Flask 部署最佳实践](https://flask.palletsprojects.com/en/3.0.x/deploying/)

## ✨ 下一步

部署成功后，你可以：
- 配置自定义域名
- 设置持续部署（CI/CD）
- 添加环境变量
- 配置团队访问权限
- 启用分析和监控

---

**需要帮助？** 查看 [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) 获取更多信息。
