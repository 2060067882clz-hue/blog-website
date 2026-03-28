# 博客项目前端说明

这是一个基于 `Vue 3 + Vite` 搭建的前端项目，当前主要完成了登录、注册、认证态持久化、个人空间展示以及基础路由守卫。页面视觉上已经统一为偏玻璃拟态的风格，登录页和个人空间页使用了同一套背景氛围、卡片质感和过渡动画。

## 1. 技术栈

- `Vue 3`
- `Vue Router`
- `Vite`
- 原生 `fetch` 进行接口请求
- `localStorage` 用于保存登录态

## 2. 运行环境

- `Node.js 18+`，建议使用较新的 LTS 版本
- `npm 9+`

## 3. 启动方式

### 安装依赖

```bash
npm install
```

### 启动开发环境

```bash
npm run dev
```

默认启动后可访问：

```text
http://localhost:5173
```

### 生产构建

```bash
npm run build
```

### 本地预览构建结果

```bash
npm run preview
```

## 4. 当前已完成功能

- 登录 / 注册双态页面
- 登录表单校验
- 注册表单校验
- 登录成功后保存 `token` 和用户信息
- 认证信息持久化到 `localStorage`
- 登录后跳转到个人入口页
- 个人空间页面展示
- 个人信息展示
- 已发布文章展示
- 收藏文章展示
- 列表分页切换
- 获取当前用户信息并同步页面
- 退出登录
- 路由守卫，未登录时限制访问 `/profile` 和 `/center`

## 5. 项目目录结构

```text
front
├─ public
│  ├─ favicon.svg
│  └─ icons.svg
├─ src
│  ├─ assets
│  │  ├─ hero.png
│  │  ├─ vite.svg
│  │  └─ vue.svg
│  ├─ router
│  │  └─ index.js
│  ├─ services
│  │  └─ auth.js
│  ├─ views
│  │  ├─ Login.vue
│  │  ├─ Profile.vue
│  │  └─ center.vue
│  ├─ App.vue
│  ├─ main.js
│  └─ style.css
├─ index.html
├─ package.json
├─ vite.config.js
└─ README.md
```

## 6. 主要页面说明

### `src/views/Login.vue`

- 登录与注册共用一个页面
- 通过按钮切换 `login / register` 模式
- 表单校验在页面内部完成
- 登录或注册成功后调用 `saveAuth` 持久化认证信息

### `src/views/Profile.vue`

- 当前是一个轻量入口页
- 点击按钮后跳转到个人空间页 `/center`

### `src/views/center.vue`

- 个人空间主页面
- 包含个人信息、我的文章、我的收藏三个模块
- 已实现分页逻辑与切换过渡
- 页面会优先读取本地用户信息，再尝试请求后端同步当前用户数据

### `src/services/auth.js`

- 封装了认证相关接口请求
- 负责保存、读取、清理 `token` 和用户信息
- 提供登录、注册、获取当前用户、退出登录等方法

## 7. 路由说明

当前前端路由如下：

- `/`：重定向到 `/login`
- `/login`：登录 / 注册页面
- `/profile`：个人入口页
- `/center`：个人空间页

路由守卫逻辑：

- 未登录时，访问 `/profile` 或 `/center` 会跳转到 `/login`
- 已登录时，访问 `/login` 会跳转到 `/profile`

## 8. 接口与后端联调说明

当前接口基础地址写在：

`src/services/auth.js`

默认值为：

```js
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
```

已接入的接口包括：

- `POST /auth/login`
- `POST /auth/register`
- `GET /auth/me`
- `POST /auth/logout`

如果后端地址或端口变化，需要同步修改 `API_BASE_URL`。

## 9. 登录态与本地存储

当前使用 `localStorage` 保存认证信息：

- `token`
- `user`

相关逻辑位于 `src/services/auth.js`：

- `saveAuth`
- `saveUser`
- `getStoredToken`
- `getStoredUser`
- `clearAuth`

## 10. 注意事项

- 项目当前没有使用 `.env` 管理接口地址，后续建议把 `API_BASE_URL` 抽到环境变量中。
- 当前请求方式是原生 `fetch`，并没有使用 `axios`。
- `package.json` 中实际只安装了 `vue` 和 `vue-router`，README 或文档里不要再写 `pinia`、`axios` 之类当前未使用的依赖。
- `dist/` 是构建产物目录，通常不建议手动修改。
- `node_modules/` 已存在，说明当前项目已经安装过依赖，但在新环境下仍建议先执行 `npm install`。
- 页面里的部分中文文本如果在某些编辑器里显示乱码，通常和文件编码或终端编码有关，建议统一使用 `UTF-8`。

## 11. 后续可优化方向

- 使用环境变量管理接口地址
- 补充文章列表和收藏列表的真实接口
- 优化 `Profile.vue`，让入口页风格与主页面完全统一
- 增加全局消息提示和错误边界处理
- 增加更完整的权限控制和用户资料编辑能力

## 12. 常用命令

```bash
# 开发
npm run dev

# 构建
npm run build

# 预览构建结果
npm run preview
```
