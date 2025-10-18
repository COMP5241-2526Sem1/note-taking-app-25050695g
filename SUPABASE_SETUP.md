# Supabase PostgreSQL 数据库集成指南

本指南将帮助你将 Note Taking App 从本地 SQLite 数据库迁移到 Supabase 托管的 PostgreSQL 数据库。

## 目录
1. [为什么使用 Supabase PostgreSQL](#为什么使用-supabase-postgresql)
2. [前置要求](#前置要求)
3. [Supabase 设置步骤](#supabase-设置步骤)
4. [本地配置](#本地配置)
5. [测试数据库连接](#测试数据库连接)
6. [故障排除](#故障排除)

## 为什么使用 Supabase PostgreSQL

- ✅ **持久化存储**：数据不会在服务器重启后丢失
- ✅ **云端托管**：无需管理数据库服务器
- ✅ **免费层级**：Supabase 提供慷慨的免费额度
- ✅ **PostgreSQL 功能**：完整的关系型数据库功能
- ✅ **易于扩展**：可以轻松升级到付费计划

## 前置要求

- Python 3.8+
- Supabase 账户（免费注册）
- 互联网连接

## Supabase 设置步骤

### 步骤 1：创建 Supabase 账户和项目

1. 访问 [Supabase](https://supabase.com) 并注册账户
2. 创建一个新项目：
   - 点击 "New Project"
   - 输入项目名称（例如：`note-taking-app`）
   - 设置数据库密码（**请妥善保管此密码**）
   - 选择最近的地区（例如：East Asia for Hong Kong）
   - 点击 "Create new project"
3. 等待项目初始化（约 2-3 分钟）

### 步骤 2：获取数据库连接字符串

1. 在 Supabase 项目仪表板中，点击左侧的 **Settings** (齿轮图标)
2. 选择 **Database**
3. 向下滚动到 **Connection string** 部分
4. 选择 **URI** 标签
5. 复制连接字符串，格式如下：
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxxx.supabase.co:5432/postgres
   ```
6. 将 `[YOUR-PASSWORD]` 替换为你在步骤 1 中设置的数据库密码

### 步骤 3：配置连接池（推荐用于生产环境）

对于生产环境，建议使用 Supabase 的连接池功能：

1. 在 **Database** 设置页面，找到 **Connection pooling** 部分
2. 选择 **Transaction** 模式
3. 复制 **Connection string** (Pooler)，格式如下：
   ```
   postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   ```

## 本地配置

### 步骤 1：安装依赖

```bash
pip install -r requirements.txt
```

这将安装以下新依赖：
- `psycopg2-binary`: PostgreSQL 数据库驱动
- `python-dotenv`: 环境变量管理

### 步骤 2：创建 .env 文件

1. 复制示例文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，添加你的 Supabase 连接字符串：
   ```bash
   # Supabase PostgreSQL Database Configuration
   DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.xxxxxxxxxxxxxx.supabase.co:5432/postgres
   
   # Flask Configuration
   SECRET_KEY=asdf#FGSgvasgf$5$WGT
   FLASK_ENV=development
   ```

3. **重要**：确保 `.env` 文件已添加到 `.gitignore`（已自动配置）

### 步骤 3：验证配置

检查 `.env` 文件内容（不要提交到 Git）：
```bash
cat .env
```

## 测试数据库连接

### 运行自动化测试脚本

我们提供了一个全面的测试脚本来验证数据库连接和功能：

```bash
python test_supabase.py
```

该脚本将测试：
1. ✅ 数据库连接
2. ✅ 表创建
3. ✅ User CRUD 操作
4. ✅ Note CRUD 操作
5. ✅ 多条记录管理

预期输出示例：
```
============================================================
  SUPABASE POSTGRESQL DATABASE TESTS
============================================================

✅ Using PostgreSQL database (Supabase)

============================================================
  Testing Database Connection
============================================================
✅ Successfully connected to database
   Database URI: postgresql:***@db.xxxxxxxxxxxxxx.supabase.co:5432/postgres

============================================================
  Testing Table Creation
============================================================
✅ Tables created successfully:
   - user
   - note

...

============================================================
  Test Summary
============================================================
✅ PASSED: Database Connection
✅ PASSED: Table Creation
✅ PASSED: User CRUD Operations
✅ PASSED: Note CRUD Operations
✅ PASSED: Multiple Notes

5/5 tests passed

🎉 All tests passed! Database is working correctly.
```

### 手动测试应用

1. 启动应用：
   ```bash
   python src/main.py
   ```

2. 应用将在 `http://localhost:5001` 运行

3. 在浏览器中打开应用，测试以下功能：
   - 创建笔记
   - 编辑笔记
   - 删除笔记
   - 搜索笔记

4. 验证数据持久化：
   - 停止应用（Ctrl+C）
   - 重新启动应用
   - 确认之前创建的笔记仍然存在

### 在 Supabase 中验证数据

1. 返回 Supabase 项目仪表板
2. 点击左侧的 **Table Editor**
3. 你应该能看到 `note` 和 `user` 表
4. 点击表名查看数据记录

## 故障排除

### 问题 1：连接被拒绝

**症状**：
```
❌ Failed to connect to database: could not connect to server
```

**解决方案**：
1. 检查互联网连接
2. 验证 Supabase 项目是否已完全初始化
3. 确认防火墙未阻止连接
4. 检查数据库密码是否正确

### 问题 2：认证失败

**症状**：
```
❌ Failed to connect to database: password authentication failed
```

**解决方案**：
1. 确认 `.env` 文件中的密码正确
2. 在 Supabase 仪表板中重置数据库密码：
   - Settings → Database → Reset Database Password
3. 更新 `.env` 文件中的连接字符串

### 问题 3：模块导入错误

**症状**：
```
ModuleNotFoundError: No module named 'psycopg2'
```

**解决方案**：
```bash
pip install -r requirements.txt
```

### 问题 4：SSL 连接错误

**症状**：
```
❌ SSL connection error
```

**解决方案**：
在连接字符串末尾添加 `?sslmode=require`：
```
DATABASE_URL=postgresql://postgres:password@host:5432/postgres?sslmode=require
```

### 问题 5：连接池耗尽

**症状**：
```
❌ remaining connection slots are reserved
```

**解决方案**：
使用 Supabase 的连接池 URL（参见步骤 3 中的配置连接池）

## 环境切换

### 使用本地 SQLite（开发）

移除或注释掉 `.env` 文件中的 `DATABASE_URL`：
```bash
# DATABASE_URL=postgresql://...
```

### 使用 Supabase PostgreSQL（生产）

在 `.env` 文件中设置 `DATABASE_URL`：
```bash
DATABASE_URL=postgresql://postgres:password@host:5432/postgres
```

## 数据库架构

应用自动创建以下表：

### User 表
```sql
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);
```

### Note 表
```sql
CREATE TABLE note (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 迁移现有数据（可选）

如果你在本地 SQLite 数据库中有现有数据，可以使用以下脚本迁移：

```python
# 创建 migrate_data.py 文件
import sqlite3
import os
from dotenv import load_dotenv
from src.main import app, db
from src.models.note import Note
from src.models.user import User

load_dotenv()

def migrate_sqlite_to_postgres():
    # 连接到本地 SQLite
    sqlite_conn = sqlite3.connect('database/app.db')
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    
    with app.app_context():
        # 迁移用户
        cursor.execute("SELECT * FROM user")
        for row in cursor.fetchall():
            user = User(id=row['id'], username=row['username'], email=row['email'])
            db.session.add(user)
        
        # 迁移笔记
        cursor.execute("SELECT * FROM note")
        for row in cursor.fetchall():
            note = Note(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            db.session.add(note)
        
        db.session.commit()
        print("Migration completed!")
    
    sqlite_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_postgres()
```

## 安全最佳实践

1. ✅ **永远不要提交 `.env` 文件到 Git**
2. ✅ **使用强密码**：Supabase 数据库密码应该复杂且唯一
3. ✅ **定期备份**：在 Supabase 仪表板中设置自动备份
4. ✅ **使用环境变量**：在生产环境中使用环境变量而不是 `.env` 文件
5. ✅ **限制数据库访问**：只允许必要的 IP 地址访问（在 Supabase 设置中配置）

## 性能优化

1. **使用连接池**：在生产环境中使用 Supabase 的连接池 URL
2. **索引优化**：为常用查询字段添加索引
3. **查询优化**：使用 SQLAlchemy 的查询优化功能
4. **缓存**：考虑添加 Redis 缓存层（未来改进）

## 监控和维护

### Supabase 仪表板功能

1. **Database Usage**：监控存储空间使用情况
2. **API Usage**：查看 API 调用统计
3. **Logs**：查看数据库日志和错误
4. **Performance**：监控查询性能

### 定期任务

- 每周检查数据库使用量
- 每月审查查询性能
- 定期测试备份恢复流程

## 下一步

- [ ] 在 Vercel 上部署应用（使用 Supabase 作为数据库）
- [ ] 添加用户认证功能
- [ ] 实现数据备份策略
- [ ] 添加 API 速率限制
- [ ] 配置 CI/CD 流水线

## 获取帮助

- Supabase 文档：https://supabase.com/docs
- Flask-SQLAlchemy 文档：https://flask-sqlalchemy.palletsprojects.com/
- PostgreSQL 文档：https://www.postgresql.org/docs/

## 更新日志

- **2025-10-18**: 初始版本，添加 Supabase PostgreSQL 支持
