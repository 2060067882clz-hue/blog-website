# 数据库对接说明

当前认证模块先使用内存仓储实现，便于前后端联调。后续数据库同学可以按下列字段和仓储能力替换为 MySQL 实现。

## users 表建议字段

- `id`: 整数主键，自增
- `username`: 字符串，唯一，用于登录
- `password`: 字符串，存储加密后的密码
- `email`: 字符串，唯一或按业务约束处理
- `role`: 整数或枚举，`0` 为普通用户，`1` 为管理员
- `create_time`: 时间戳，注册时间

## articles 表建议字段

- `id`: 整数主键，自增
- `title`: 字符串
- `content`: 长文本
- `author_id`: 整数外键，关联 `users.id`
- `create_time`: 时间戳
- `update_time`: 时间戳

## comments 表建议字段

- `id`: 整数主键，自增
- `article_id`: 整数外键，关联 `articles.id`
- `user_id`: 整数外键，关联 `users.id`
- `content`: 文本
- `create_time`: 时间戳

## 用户仓储需要提供的能力

- `get_by_id(user_id)`
- `get_by_username(username)`
- `get_by_email(email)`
- `create_user(payload)`
- `list_users()`

## token 仓储需要提供的能力

- `revoke(token, expires_at)`
- `is_revoked(token)`
- `cleanup_expired()`

## 当前约定

- 认证方式使用 `Authorization: Bearer <token>`
- 注册接口成功后直接返回登录 token
- 退出登录通过失效 token 实现
- 文章和评论当前使用内存仓储实现，接口完成后可平滑替换为 MySQL 持久化版本
- 当前仓库已经补充了 MySQL 仓储实现和建表脚本，脚本见 [mysql_schema.sql](/Users/strawverry/blog-website/backend/docs/mysql_schema.sql)
