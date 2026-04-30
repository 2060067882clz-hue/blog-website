# Blog Backend

基于 FastAPI 的博客网站后端骨架，当前完成了文档要求的认证模块和健康检查模块。

## 技术栈

- Python 3.9+
- FastAPI
- Uvicorn
- Pydantic

## 快速启动

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

如果要切到 MySQL，请先：

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS blog_website CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

然后把 `.env` 里的 `DB_BACKEND` 改成 `mysql`，并配置好 `MYSQL_HOST`、`MYSQL_PORT`、`MYSQL_USER`、`MYSQL_PASSWORD`、`MYSQL_DATABASE`。应用启动时会自动执行 [mysql_schema.sql](/Users/strawverry/blog-website/backend/docs/mysql_schema.sql) 并初始化演示数据。

也可以直接运行：

```bash
python app/main.py
```

## 演示账号

- 用户名：`admin`
- 密码：`Admin123456`

## 存储模式

- `DB_BACKEND=memory`
  用于本地快速开发，数据保存在内存中，服务重启后会丢失。
- `DB_BACKEND=mysql`
  使用 MySQL 持久化用户、文章、评论和失效 token。

## 已实现接口

- `GET /`
- `GET /api/v1/health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`
- `GET /api/v1/articles`
- `GET /api/v1/articles/me`
- `POST /api/v1/articles`
- `GET /api/v1/articles/{article_id}`
- `PATCH /api/v1/articles/{article_id}`
- `DELETE /api/v1/articles/{article_id}`
- `GET /api/v1/articles/{article_id}/comments`
- `POST /api/v1/articles/{article_id}/comments`
- `DELETE /api/v1/comments/{comment_id}`
- `GET /api/v1/admin/users`
- `GET /api/v1/admin/articles`
- `DELETE /api/v1/admin/users/{user_id}`
- `DELETE /api/v1/admin/articles/{article_id}`
