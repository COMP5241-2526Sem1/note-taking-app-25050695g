# Supabase PostgreSQL 快速配置指南

## 1. 获取 Supabase 数据库连接字符串

### 1.1 登录 Supabase
访问 https://supabase.com 并登录

### 1.2 创建或选择项目
- 如果没有项目，点击 "New Project"
- 设置项目名称和数据库密码（**记住这个密码！**）
- 选择地区（推荐：East Asia - Singapore）
- 等待约 2-3 分钟完成初始化

### 1.3 获取连接字符串
1. 进入项目仪表板
2. 左侧菜单点击 **Settings** (⚙️)
3. 选择 **Database**
4. 滚动到 **Connection string** 部分
5. 选择 **URI** 标签
6. 复制连接字符串

连接字符串格式：
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

**重要**：将 `[YOUR-PASSWORD]` 替换为你的实际数据库密码

## 2. 本地配置（3 步完成）

### 步骤 1：安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 2：创建 .env 文件
```bash
cp .env.example .env
```

### 步骤 3：配置 .env 文件
编辑 `.env` 文件，添加你的连接字符串：

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
SECRET_KEY=asdf#FGSgvasgf$5$WGT
FLASK_ENV=development
```

**替换**：
- `YOUR_PASSWORD` → 你的实际数据库密码
- `xxxxxxxxxxxxx` → 你的 Supabase 项目 ID

## 3. 测试数据库连接

### 运行测试脚本
```bash
python test_supabase.py
```

预期输出：
```
✅ Successfully connected to database
✅ Tables created successfully
✅ PASSED: User CRUD Operations
✅ PASSED: Note CRUD Operations
🎉 All tests passed!
```

### 启动应用
```bash
python src/main.py
```

访问：http://localhost:5001

## 4. 验证数据在 Supabase 中

1. 返回 Supabase 项目仪表板
2. 点击左侧 **Table Editor**
3. 查看 `note` 和 `user` 表
4. 确认你在应用中创建的数据显示在这里

## 常见问题快速修复

### ❌ 连接失败
```bash
# 检查密码是否正确
cat .env | grep DATABASE_URL

# 重新安装依赖
pip install -r requirements.txt
```

### ❌ 认证失败
- 在 Supabase 仪表板重置密码：Settings → Database → Reset Password
- 更新 `.env` 文件中的连接字符串

### ❌ 模块未找到
```bash
pip install psycopg2-binary python-dotenv
```

## 环境变量优先级

```
1. DATABASE_URL (设置后使用 Supabase PostgreSQL)
2. VERCEL (在 Vercel 部署时使用内存数据库)
3. 本地开发 (使用本地 SQLite database/app.db)
```

## 切换数据库

### 使用 Supabase PostgreSQL
```bash
# .env 文件中设置
DATABASE_URL=postgresql://postgres:password@host:5432/postgres
```

### 使用本地 SQLite
```bash
# .env 文件中注释或删除 DATABASE_URL
# DATABASE_URL=...
```

## 下一步：部署到 Vercel

1. 在 Vercel 项目设置中添加环境变量：
   ```
   DATABASE_URL = postgresql://postgres:password@host:5432/postgres
   SECRET_KEY = asdf#FGSgvasgf$5$WGT
   ```

2. 部署：
   ```bash
   vercel --prod
   ```

## 安全提醒 🔒

- ⚠️ **永远不要**提交 `.env` 文件到 Git
- ⚠️ **不要**在代码中硬编码密码
- ⚠️ **定期**更换数据库密码
- ⚠️ **使用**强密码（建议 16+ 字符）

## 需要帮助？

查看完整文档：[SUPABASE_SETUP.md](./SUPABASE_SETUP.md)

---

## 配置检查清单 ✅

- [ ] 创建 Supabase 账户和项目
- [ ] 获取数据库连接字符串
- [ ] 安装依赖 (`pip install -r requirements.txt`)
- [ ] 创建 `.env` 文件
- [ ] 配置 `DATABASE_URL` 在 `.env` 中
- [ ] 运行测试脚本 (`python test_supabase.py`)
- [ ] 启动应用并测试功能
- [ ] 在 Supabase Table Editor 中验证数据
- [ ] (可选) 部署到 Vercel 并配置环境变量
