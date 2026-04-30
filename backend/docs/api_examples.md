# API 调用示例

以下示例默认服务运行在：

```bash
http://127.0.0.1:8000
```

接口前缀为：

```bash
/api/v1
```

## 1. 健康检查

```bash
curl http://127.0.0.1:8000/api/v1/health
```

## 2. 登录

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin123456"
  }'
```

## 3. 注册

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tester01",
    "password": "Tester123",
    "email": "tester01@example.com",
    "nickname": "测试用户"
  }'
```

## 4. 获取当前用户

```bash
curl http://127.0.0.1:8000/api/v1/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

## 5. 获取文章列表

```bash
curl http://127.0.0.1:8000/api/v1/articles
```

## 6. 发布文章

```bash
curl -X POST http://127.0.0.1:8000/api/v1/articles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "title": "后端联调示例文章",
    "content": "这篇文章用于演示文章发布接口。"
  }'
```

## 7. 更新文章

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/articles/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "title": "更新后的标题"
  }'
```

## 8. 获取文章评论

```bash
curl http://127.0.0.1:8000/api/v1/articles/1/comments
```

## 9. 发表评论

```bash
curl -X POST http://127.0.0.1:8000/api/v1/articles/1/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "content": "这是一条测试评论。"
  }'
```

## 10. 查看管理员用户列表

```bash
curl http://127.0.0.1:8000/api/v1/admin/users \
  -H "Authorization: Bearer <TOKEN>"
```

## 11. 查看管理员文章列表

```bash
curl http://127.0.0.1:8000/api/v1/admin/articles \
  -H "Authorization: Bearer <TOKEN>"
```

## 12. 删除评论

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/comments/1 \
  -H "Authorization: Bearer <TOKEN>"
```

## 13. 删除文章

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/articles/1 \
  -H "Authorization: Bearer <TOKEN>"
```
