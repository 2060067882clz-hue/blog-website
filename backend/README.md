# Blog Backend

博客项目后端服务，基于 `FastAPI` 搭建，当前已经完成用户认证、文章、评论、管理员管理和 MySQL 持久化接入。

## 当前完成内容

- 用户认证：注册、登录、退出登录、获取当前用户
- 文章模块：列表、详情、发布、修改、删除、我的文章
- 评论模块：按文章查询、发表评论、删除评论
- 管理员模块：查看用户、查看文章、删除用户、删除文章
- 存储模式：支持 `memory` 和 `mysql` 两种运行方式

## 技术栈

- Python 3.9+
- FastAPI
- Uvicorn
- Pydantic
- PyMySQL
- python-dotenv

## 目录结构

```text
backend
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── app
│   ├── main.py
│   ├── api
│   │   ├── deps.py
│   │   ├── router.py
│   │   └── routes
│   │       ├── admin.py
│   │       ├── articles.py
│   │       ├── auth.py
│   │       ├── comments.py
│   │       └── health.py
│   ├── core
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── security.py
│   ├── models
│   ├── repositories
│   ├── schemas
│   └── services
└── docs
    ├── api_examples.md
    ├── database_contract.md
    └── mysql_schema.sql
```

## 快速启动

### 方式一：内存模式

适合快速演示和前后端本地联调，服务重启后数据会丢失。

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

默认配置里 `DB_BACKEND=memory`，无需改数据库参数即可直接启动。

### 方式二：MySQL 模式

适合组内联调和阶段性验收，用户、文章、评论、失效 token 会持久化到数据库。

1. 创建数据库

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS blog_website CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
```

2. 复制环境变量并修改存储模式

```bash
cp .env.example .env
```

把 `.env` 中的以下配置改成可用值：

```env
DB_BACKEND=mysql
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的数据库密码
MYSQL_DATABASE=blog_website
```

3. 启动服务

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

首次启动时会自动执行 [docs/mysql_schema.sql](docs/mysql_schema.sql) 并初始化演示数据。

## 环境变量说明

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| `APP_NAME` | 服务名 | `Blog Website Backend` |
| `APP_VERSION` | 版本号 | `1.0.0` |
| `API_V1_PREFIX` | 接口前缀 | `/api/v1` |
| `HOST` | 监听地址 | `127.0.0.1` |
| `PORT` | 服务端口 | `8000` |
| `DB_BACKEND` | 存储模式，`memory` 或 `mysql` | `memory` |
| `MYSQL_HOST` | MySQL 主机 | `127.0.0.1` |
| `MYSQL_PORT` | MySQL 端口 | `3306` |
| `MYSQL_USER` | MySQL 用户名 | `root` |
| `MYSQL_PASSWORD` | MySQL 密码 | `123456` |
| `MYSQL_DATABASE` | MySQL 数据库名 | `blog_website` |
| `MYSQL_CHARSET` | MySQL 字符集 | `utf8mb4` |
| `SECRET_KEY` | token 签名密钥 | `change-me-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | token 有效期，单位分钟 | `10080` |
| `DEMO_ADMIN_USERNAME` | 演示管理员用户名 | `admin` |
| `DEMO_ADMIN_PASSWORD` | 演示管理员密码 | `Admin123456` |
| `DEMO_ADMIN_EMAIL` | 演示管理员邮箱 | `admin@example.com` |
| `DEMO_ADMIN_NICKNAME` | 演示管理员昵称 | `博客管理员` |

## 演示账号

- 用户名：`admin`
- 密码：`Admin123456`

## 接口总览

### 基础与认证

- `GET /`
- `GET /api/v1/health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### 文章

- `GET /api/v1/articles`
- `GET /api/v1/articles/me`
- `POST /api/v1/articles`
- `GET /api/v1/articles/{article_id}`
- `PATCH /api/v1/articles/{article_id}`
- `DELETE /api/v1/articles/{article_id}`

### 评论

- `GET /api/v1/articles/{article_id}/comments`
- `POST /api/v1/articles/{article_id}/comments`
- `DELETE /api/v1/comments/{comment_id}`

### 管理员

- `GET /api/v1/admin/users`
- `GET /api/v1/admin/articles`
- `DELETE /api/v1/admin/users/{user_id}`
- `DELETE /api/v1/admin/articles/{article_id}`

常用联调命令见 [docs/api_examples.md](docs/api_examples.md)。

## 协作说明

- 本地敏感配置写在 `.env`，不要提交到仓库
- 虚拟环境目录 `.venv/` 不要提交到仓库
- 当前仓储层已经抽象成接口，后续如果要切 ORM 或 Redis，可以优先从 `repositories/` 替换
- 管理员账号、初始化文章和初始化评论由启动阶段自动补齐，便于新同学拉代码后马上联调
- 如果只改后端逻辑，建议优先补 `services/` 和 `repositories/` 的说明，再动路由层

## 相关文档

- 数据库字段与仓储约定：[docs/database_contract.md](docs/database_contract.md)
- MySQL 建表脚本：[docs/mysql_schema.sql](docs/mysql_schema.sql)
- API 调用示例：[docs/api_examples.md](docs/api_examples.md)
