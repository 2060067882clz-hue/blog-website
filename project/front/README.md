# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).


博客项目前端说明
博客网站小组作业的前端项目，当前阶段重点完成认证模块界面与交互，已经支持注册、登录、退出登录、获取当前用户信息，并与后端认证接口完成对接。

技术栈
Vue 3 + Composition API

Vite - 构建工具

Axios - HTTP 请求库

Vue Router - 路由管理

Pinia - 状态管理

当前已完成功能
✅ 项目初始化（Vite + Vue 3）

✅ 路由配置（公开路由 + 认证路由守卫）

✅ Axios 封装（请求/响应拦截器、Token 自动携带）

✅ 状态管理（用户信息、Token 持久化）

✅ 登录页面与交互

✅ 注册页面与交互

✅ 退出登录功能

✅ 获取当前用户信息

✅ 全局错误处理（网络错误、业务错误、401 自动跳转）

✅ 页面加载状态

✅ 表单验证

快速启动
环境要求
Node.js 18+

npm 或 pnpm

安装与运行
bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 复制环境变量文件（如果存在 .env.example）
cp .env.example .env

# 启动开发服务器
npm run dev
开发服务器启动后，访问 http://localhost:5173
