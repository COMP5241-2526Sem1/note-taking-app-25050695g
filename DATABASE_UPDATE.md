# 数据库配置更新说明

## 重要更新 🎉

应用程序现已支持 **Supabase PostgreSQL** 数据库！

### 新增功能

1. ✅ **支持外部 PostgreSQL 数据库**（Supabase）
2. ✅ **数据持久化**：数据不会在重启后丢失
3. ✅ **环境配置管理**：使用 `.env` 文件
4. ✅ **自动化测试**：数据库连接和功能测试
5. ✅ **数据迁移工具**：从 SQLite 迁移到 PostgreSQL

### 文件更新

#### 新增文件
- `.env.example` - 环境变量模板
- `.gitignore` - Git 忽略文件配置
- `src/config.py` - 数据库配置模块
- `test_supabase.py` - 数据库测试脚本
- `migrate_to_supabase.py` - 数据迁移脚本
- `SUPABASE_SETUP.md` - 详细设置指南
- `SUPABASE_QUICK_START.md` - 快速入门指南
- `DATABASE_UPDATE.md` - 本文件

#### 修改文件
- `requirements.txt` - 添加 `psycopg2-binary` 和 `python-dotenv`
- `src/main.py` - 重构数据库配置逻辑

### 数据库配置优先级

应用程序按以下优先级选择数据库：

1. **DATABASE_URL 环境变量**（Supabase PostgreSQL）
   - 当设置 `DATABASE_URL` 时使用
   - 推荐用于生产环境

2. **Vercel 环境**（内存数据库）
   - 当 `VERCEL=1` 且无 `DATABASE_URL` 时使用
   - 数据不持久化

3. **本地开发**（SQLite）
   - 默认使用 `database/app.db`
   - 适合开发和测试

### 快速开始

#### 选项 A：使用 Supabase PostgreSQL（推荐）

1. 按照 [SUPABASE_QUICK_START.md](./SUPABASE_QUICK_START.md) 设置 Supabase
2. 创建 `.env` 文件并配置 `DATABASE_URL`
3. 运行测试：`python test_supabase.py`
4. 启动应用：`python src/main.py`

#### 选项 B：使用本地 SQLite（开发）

1. 不创建 `.env` 文件或不设置 `DATABASE_URL`
2. 直接运行：`python src/main.py`
3. 数据保存在 `database/app.db`

### 安装依赖

```bash
pip install -r requirements.txt
```

新增依赖：
- `psycopg2-binary` - PostgreSQL 数据库驱动
- `python-dotenv` - 环境变量管理

### 测试数据库

运行完整测试套件：

```bash
python test_supabase.py
```

测试内容：
- ✅ 数据库连接
- ✅ 表创建
- ✅ User CRUD 操作
- ✅ Note CRUD 操作
- ✅ 多条记录管理

### 迁移现有数据

如果你有本地 SQLite 数据想迁移到 Supabase：

```bash
python migrate_to_supabase.py
```

此脚本会：
1. 检查环境配置
2. 连接两个数据库
3. 迁移所有用户和笔记
4. 提供详细的迁移报告

### 环境变量

在 `.env` 文件中配置（参考 `.env.example`）：

```env
# Supabase PostgreSQL
DATABASE_URL=postgresql://postgres:your_password@db.xxxxx.supabase.co:5432/postgres

# Flask 配置
SECRET_KEY=asdf#FGSgvasgf$5$WGT
FLASK_ENV=development
```

### 安全注意事项 🔒

1. ⚠️ **永远不要提交 `.env` 文件到 Git**
2. ⚠️ `.env` 已添加到 `.gitignore`
3. ⚠️ 使用强密码保护数据库
4. ⚠️ 在生产环境使用环境变量而非 `.env` 文件

### 部署到 Vercel

在 Vercel 项目设置中添加环境变量：

```
DATABASE_URL = your_supabase_connection_string
SECRET_KEY = your_secret_key
```

然后部署：

```bash
vercel --prod
```

### 故障排除

#### 问题：连接失败
```bash
# 检查配置
cat .env

# 验证 Python 包
pip list | grep psycopg2
```

#### 问题：导入错误
```bash
# 重新安装依赖
pip install -r requirements.txt
```

#### 问题：认证失败
- 在 Supabase 仪表板重置密码
- 更新 `.env` 中的 `DATABASE_URL`

### 文档资源

- 📖 [快速入门指南](./SUPABASE_QUICK_START.md)
- 📖 [详细设置指南](./SUPABASE_SETUP.md)
- 📖 [Supabase 文档](https://supabase.com/docs)
- 📖 [Flask-SQLAlchemy 文档](https://flask-sqlalchemy.palletsprojects.com/)

### 代码示例

#### 数据库配置（src/config.py）

```python
from src.config import get_database_config

# 获取数据库配置
db_config = get_database_config()

# 配置包含：
# - SQLALCHEMY_DATABASE_URI
# - SQLALCHEMY_TRACK_MODIFICATIONS
# - SQLALCHEMY_ENGINE_OPTIONS
```

#### 环境变量加载（src/main.py）

```python
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 使用环境变量
database_url = os.environ.get('DATABASE_URL')
```

### 架构改进

#### 之前
```
src/main.py
└── 硬编码数据库配置
    ├── if DATABASE_URL: use external
    ├── elif VERCEL: use memory
    └── else: use SQLite
```

#### 现在
```
src/main.py
├── 加载 .env
├── 导入 config.py
└── 使用 get_database_config()

src/config.py
└── 集中管理数据库配置
    ├── 环境检测
    ├── URL 格式化
    └── 连接池配置
```

### 性能优化

新配置包含以下优化：

1. **连接池预检查**（`pool_pre_ping`）
   - 使用前验证连接有效性
   - 防止使用断开的连接

2. **连接回收**（`pool_recycle`）
   - 5分钟后回收连接
   - 防止长时间空闲连接

3. **URL 格式化**
   - 自动转换 `postgres://` 为 `postgresql://`
   - 兼容 Supabase 连接字符串

### 下一步

- [ ] 配置 Supabase 数据库
- [ ] 运行测试验证功能
- [ ] 迁移现有数据（如有）
- [ ] 部署到生产环境
- [ ] 配置数据库备份
- [ ] 实现用户认证

### 支持

如果遇到问题：

1. 查看 [SUPABASE_QUICK_START.md](./SUPABASE_QUICK_START.md)
2. 查看 [SUPABASE_SETUP.md](./SUPABASE_SETUP.md)
3. 运行 `python test_supabase.py` 诊断问题

---

**更新日期**：2025-10-18
**版本**：2.0.0
**作者**：Database Refactoring Team
