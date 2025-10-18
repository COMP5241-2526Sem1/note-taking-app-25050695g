# Vercel 部署指南

## 准备工作

代码已经配置好，可以直接部署到 Vercel。

## 部署步骤

### 方法一：通过 GitHub（推荐）

1. **将代码推送到 GitHub**
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. **登录 Vercel**
   - 访问 https://vercel.com/
   - 使用 GitHub 账号登录

3. **导入项目**
   - 点击 "Add New..." → "Project"
   - 选择你的 GitHub 仓库：`note-taking-app-updated-xxwtiancai`
   - 点击 "Import"

4. **配置项目**
   - Project Name: 保持默认或自定义
   - Framework Preset: 选择 "Other"
   - Root Directory: 保持默认 `./`
   - Build Command: 留空
   - Output Directory: 留空
   - Install Command: `pip install -r requirements.txt`

5. **环境变量（可选）**
   如果你想使用外部数据库（如 PostgreSQL），添加环境变量：
   - Key: `DATABASE_URL`
   - Value: 你的数据库连接字符串

6. **部署**
   - 点击 "Deploy" 按钮
   - 等待部署完成（通常需要 1-2 分钟）

### 方法二：通过 Vercel CLI

1. **安装 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **登录 Vercel**
   ```bash
   vercel login
   ```

3. **部署**
   ```bash
   cd /Users/xiongweixiao/Desktop/polyu-msc/COMP5241/lab2/note-taking-app-updated-xxwtiancai
   vercel
   ```
   
   按照提示操作：
   - Set up and deploy? Y
   - Which scope? 选择你的账号
   - Link to existing project? N
   - What's your project's name? 输入项目名称或按回车使用默认
   - In which directory is your code located? ./
   - 等待部署完成

4. **生产环境部署**
   ```bash
   vercel --prod
   ```

## 重要说明

### 数据库配置

当前配置使用以下策略：

1. **生产环境（Vercel）**：
   - 如果设置了 `DATABASE_URL` 环境变量，使用外部数据库
   - 否则使用内存数据库（数据在每次部署后会丢失）

2. **本地开发**：
   - 使用 SQLite 文件数据库（`database/app.db`）

### 使用外部数据库（推荐用于生产）

由于 Vercel 是无服务器环境，每次请求可能在不同的实例上运行，建议使用外部数据库：

#### 免费数据库选项：

1. **Neon (PostgreSQL)** - https://neon.tech
   - 注册账号
   - 创建项目
   - 复制连接字符串
   - 在 Vercel 项目设置中添加环境变量 `DATABASE_URL`

2. **PlanetScale (MySQL)** - https://planetscale.com
   - 类似步骤

3. **Railway (PostgreSQL/MySQL)** - https://railway.app
   - 类似步骤

#### 添加环境变量到 Vercel：

1. 进入 Vercel 项目设置
2. 点击 "Settings" → "Environment Variables"
3. 添加：
   - Name: `DATABASE_URL`
   - Value: `postgresql://user:password@host:port/database` 或其他数据库连接字符串
4. 点击 "Save"
5. 重新部署项目

### 注意事项

- 如果使用内存数据库，数据会在每次部署或函数重启后丢失
- 建议在生产环境使用外部数据库服务
- Vercel 免费计划有使用限制，请查看：https://vercel.com/docs/limits

## 验证部署

部署成功后，Vercel 会提供一个 URL，例如：
- `https://your-project-name.vercel.app`

访问该 URL 测试应用功能：
- 主页应该显示笔记应用界面
- 测试创建、编辑、删除笔记功能
- 检查搜索功能是否正常

## 自定义域名（可选）

1. 在 Vercel 项目设置中点击 "Domains"
2. 添加你的自定义域名
3. 按照提示配置 DNS 记录

## 故障排除

### 部署失败
- 检查 requirements.txt 中的依赖是否正确
- 查看 Vercel 部署日志中的错误信息

### 应用无法访问
- 检查 vercel.json 配置是否正确
- 确认 api/index.py 文件存在

### 数据库错误
- 如果使用外部数据库，确认 DATABASE_URL 环境变量配置正确
- 检查数据库连接字符串格式

## 更新应用

### 通过 GitHub
- 推送新代码到 GitHub
- Vercel 会自动检测并重新部署

### 通过 CLI
```bash
vercel --prod
```

## 相关文档

- Vercel 官方文档: https://vercel.com/docs
- Vercel Python 运行时: https://vercel.com/docs/functions/runtimes/python
- Flask 部署指南: https://flask.palletsprojects.com/en/3.0.x/deploying/
