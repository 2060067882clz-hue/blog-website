# 数据库对接说明

这份文档用于说明当前后端对用户表和数据访问层的基本要求，方便数据库同学后续接入真实数据库实现。

## 建议的用户表字段

- `id`：字符串主键，建议使用 UUID
- `username`：用户名（后台自动分配的名字），必须唯一，用于登录
- `display_name`：用户展示名(用户自己取的名字)，供前端页面显示
- `password_hash`：密码哈希值，严禁存储明文密码
- `role`：用户角色，例如 `admin` 或 `user`
- `is_active`：账号是否启用，布尔值，默认为 `true`

## 数据库仓储层需要提供的方法

对于用户登陆模块，数据库提供以下方法：

- `get_by_username(username: str) -> Optional[User]`
作用：根据用户名查询用户，供登录时校验账号密码使用

- `get_by_id(user_id: str) -> Optional[User]`
作用：根据用户 ID 查询用户，供 `me` 接口根据 token 中的用户 ID 获取用户信息

- `exists_by_username(username: str) -> bool`
作用：注册时检查用户名是否已存在，避免重复创建账号

- `create_user(payload: RegisterRequest) -> User`
作用：创建新用户，并返回创建完成后的用户对象

## 当前接口对应的数据流程

- `POST /api/v1/auth/register`
作用：创建新用户，并直接返回登录 token

- `POST /api/v1/auth/login`
作用：校验用户名和密码，登录成功后返回 token

- `GET /api/v1/auth/me`
作用：根据 Bearer Token 解析出用户 ID，再查询当前用户信息

- `POST /api/v1/auth/logout`
作用：让当前 token 失效。当前阶段是在内存中记录失效 token，后续可以迁移到 Redis

## 对接说明

当前项目里的用户数据访问实现位于 `app/repositories/user_repository.py`，现在使用的是内存版实现，仅用于前后端早期联调。

等数据库准备好真实表结构后，只需要把这里的内存实现替换成数据库实现，并保证方法签名和返回结果保持一致，服务层和路由层代码原则上不需要改动。

## 建议

1. 用户名字段加唯一索引，避免并发注册时出现重复数据。
2. `password_hash` 建议字段长度预留充足，避免后续哈希算法升级时长度不够。
3. 如果后续要支持多端登录或 token 持久化，建议把 token 黑名单存储迁移到 Redis。
