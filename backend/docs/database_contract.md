# 数据库对接说明

这份文档用于后端同学和数据库同学协作时统一字段、接口能力和替换边界。当前仓库已经支持：

- `memory` 模式：便于本地快速跑通
- `mysql` 模式：便于多人联调和持久化验证

后续如果要继续演进成 ORM 或正式数据库方案，优先保持这里的字段和仓储能力不变。

## 表结构约定

### users

- `id`: 整数主键，自增
- `username`: 字符串，唯一，用于登录
- `password`: 字符串，存储加密后的密码
- `email`: 字符串，唯一
- `role`: 整数，`0` 为普通用户，`1` 为管理员
- `nickname`: 字符串，用户昵称
- `create_time`: 时间戳，注册时间

### articles

- `id`: 整数主键，自增
- `title`: 字符串，文章标题
- `content`: 长文本，文章正文
- `author_id`: 整数外键，关联 `users.id`
- `create_time`: 时间戳，创建时间
- `update_time`: 时间戳，更新时间

### comments

- `id`: 整数主键，自增
- `article_id`: 整数外键，关联 `articles.id`
- `user_id`: 整数外键，关联 `users.id`
- `content`: 文本，评论内容
- `create_time`: 时间戳，评论时间

### revoked_tokens

- `token`: 字符串主键，用于标记失效 token
- `expires_at`: 时间戳，token 原始过期时间
- `create_time`: 时间戳，失效记录写入时间

## 仓储层能力约定

### UserRepository

- `get_by_id(user_id)`
- `get_by_username(username)`
- `get_by_email(email)`
- `create_user(payload)`
- `list_users()`
- `delete_user(user_id)`

### ArticleRepository

- `list_articles()`
- `list_by_author(author_id)`
- `get_by_id(article_id)`
- `create_article(payload)`
- `update_article(article)`
- `delete_article(article_id)`

### CommentRepository

- `list_by_article(article_id)`
- `get_by_id(comment_id)`
- `create_comment(payload)`
- `delete_comment(comment_id)`
- `delete_by_article(article_id)`
- `delete_by_user(user_id)`

### TokenRepository

- `revoke(token, expires_at)`
- `is_revoked(token)`
- `cleanup_expired()`

## 当前实现说明

- MySQL 建表脚本见 [mysql_schema.sql](mysql_schema.sql)
- 当前接口认证方式统一使用 `Authorization: Bearer <token>`
- 注册成功后直接返回登录 token
- 退出登录通过失效 token 实现
- 删除用户、删除文章时，评论数据需要同步清理
- `app/api/deps.py` 中已经实现 `memory/mysql` 双模式注入，后续切换数据库时尽量不要改服务层接口
