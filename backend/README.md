# 博客项目后端说明

博客网站小组作业的后端项目，当前阶段重点完成认证模块骨架，已经支持注册、登录、退出登录、获取当前用户信息。

## 技术栈

- Python 3.9+
- FastAPI
- Uvicorn
- Pydantic

## 当前已完成功能

- FastAPI 应用初始化
- 统一异常处理
- CORS 跨域配置
- 注册、登录、退出登录、获取当前用户接口
- 基于内存的用户仓储和 token 仓储
- 演示账号初始化
- 基础配置文件读取

## 快速启动

1. 进入后端目录

```bash
cd backend
```

2. 创建虚拟环境

```bash
python3 -m venv .venv
```

3. 激活虚拟环境

```bash
source .venv/bin/activate
```

4. 安装依赖

```bash
pip install -r requirements.txt
```

5. 复制环境变量文件

```bash
cp .env.example .env
```

6. 启动项目

```bash
uvicorn app.main:app --reload
```

也可以直接运行入口文件：

```bash
python app/main.py
```

## 演示账号

- 用户名：`admin`
- 密码：`Admin123456`

可以在 `.env` 中修改默认演示账号。

## 接口列表

- `GET /`
作用：确认后端服务是否启动成功

- `GET /api/v1/health`
作用：健康检查，返回服务名、版本号和状态

- `POST /api/v1/auth/register`
作用：注册新用户，并直接返回登录 token

- `POST /api/v1/auth/login`
作用：用户登录，返回 token 和当前用户信息

- `POST /api/v1/auth/logout`
作用：退出登录，使当前 token 失效

- `GET /api/v1/auth/me`
作用：获取当前登录用户信息

## 目录结构

```text
backend
├── .env.example
├── README.md
├── requirements.txt
├── docs
│   └── database_contract.md
└── app
    ├── main.py
    ├── api
    │   ├── deps.py
    │   ├── router.py
    │   └── routes
    │       ├── auth.py
    │       └── health.py
    ├── core
    │   ├── config.py
    │   ├── exceptions.py
    │   └── security.py
    ├── models
    │   └── user.py
    ├── repositories
    │   ├── token_repository.py
    │   └── user_repository.py
    ├── schemas
    │   ├── auth.py
    │   └── common.py
    └── services
        └── auth_service.py
```

## 各文件主要功能

- `.env.example`
作用：提供项目运行所需环境变量模板，例如应用名、接口前缀、密钥和演示账号。

- `requirements.txt`
作用：记录当前后端项目依赖，方便统一安装运行环境。

- `docs/database_contract.md`
作用：写给数据库同学的对接说明，约定用户表字段和仓储接口能力。

- `app/main.py`
作用：项目入口文件，负责创建 FastAPI 应用、挂载中间件、注册异常处理器和总路由。

- `app/api/router.py`
作用：汇总所有子路由，是路由层的总入口。

- `app/api/deps.py`
作用：集中管理依赖注入，包括认证服务、用户仓储、token 仓储和 Bearer Token 提取。

- `app/api/routes/auth.py`
作用：定义认证相关接口，包括注册、登录、退出登录和获取当前用户。

- `app/api/routes/health.py`
作用：定义健康检查接口，用于确认服务是否正常运行。

- `app/core/config.py`
作用：集中读取和管理配置项，统一处理 `.env` 文件和环境变量。

- `app/core/exceptions.py`
作用：定义项目自定义异常，保证后端错误响应格式统一。

- `app/core/security.py`
作用：封装密码哈希、密码校验、token 生成和 token 解析逻辑。

- `app/models/user.py`
作用：定义用户实体，是仓储层和服务层之间传递的核心数据结构。

- `app/repositories/user_repository.py`
作用：定义用户仓储抽象接口，并提供当前阶段的内存版实现。

- `app/repositories/token_repository.py`
作用：定义 token 仓储抽象接口，并提供当前阶段的内存版失效 token 存储。

- `app/schemas/auth.py`
作用：定义认证模块接口的请求体和响应体数据结构。

- `app/schemas/common.py`
作用：定义通用接口返回结构，目前主要用于健康检查接口。

- `app/services/auth_service.py`
作用：实现认证核心业务逻辑，把路由层和仓储层衔接起来。

## 当前代码分层说明

- 路由层 `api/routes`
负责接收 HTTP 请求、调用服务层、返回接口响应。

- 服务层 `services`
负责处理业务逻辑，例如注册校验、登录校验、token 生成、退出登录。

- 仓储层 `repositories`
负责访问数据源。当前先使用内存实现，后续可以替换为 MySQL、SQLite 或 Redis。

- 模型层 `models`
负责定义系统内部的数据对象。

- 数据校验层 `schemas`
负责约束接口输入输出格式，方便前后端联调。

- 核心工具层 `core`
负责配置、异常、安全等全局公共能力。

## 后续建议

1. 将 `InMemoryUserRepository` 替换成真实数据库实现。
2. 将 `InMemoryTokenRepository` 替换成 Redis 等可持久化方案。
3. 增加刷新 token、重置密码、修改密码等功能。
4. 补充单元测试和接口测试。
