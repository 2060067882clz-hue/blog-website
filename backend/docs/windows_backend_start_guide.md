# Windows 后端启动说明

这份文档专门说明一件事：

- 这些命令应该在哪里执行
- 在 Windows PowerShell 里应该怎么执行

适用目录：

- 项目根目录：`D:\front`
- 后端目录：`D:\front\backend`

## 先分清两类命令

README 里的命令其实分成两类：

1. 项目命令
这些命令在项目终端里执行，位置通常是 `D:\front\backend`。

2. 数据库命令
这些命令用来创建 MySQL 数据库，需要在能运行 `mysql` 的终端里执行。

## 你应该在哪打开终端

如果你用的是 VS Code 或类似 IDE，最简单的方法是：

1. 打开项目文件夹 `D:\front`
2. 点击菜单 `Terminal` -> `New Terminal`
3. 默认会打开一个 PowerShell 终端

看到提示符类似下面这样就对了：

```powershell
PS D:\front>
```

## 一、后端项目命令在哪里执行

后端相关命令都建议在下面这个目录执行：

```powershell
PS D:\front\backend>
```

如果你当前终端在项目根目录 `D:\front`，先执行：

```powershell
cd .\backend
```

执行后应该变成：

```powershell
PS D:\front\backend>
```

后面这些命令都在这里执行。

## 二、数据库命令在哪里执行

创建数据库的命令是：

```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS blog_website CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
```

这条命令不是必须在 `D:\front\backend` 执行，它可以在任意目录执行，但是有一个前提：

- 你的电脑已经安装 MySQL
- `mysql` 命令已经加入系统环境变量 PATH

也就是说，只要这个命令能被终端识别，你在 `D:\front`、`D:\front\backend`、桌面目录执行都可以。

## 三、推荐的实际操作方式

最推荐你在 Windows 下这样做：

### 方案 A：全部在 PowerShell 中执行

适合你已经装好了 MySQL，而且终端里能直接运行 `mysql`。

#### 1. 进入后端目录

```powershell
cd D:\front\backend
```

#### 2. 创建并激活虚拟环境

如果还没有可用的虚拟环境：

```powershell
py -3.9 -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 提示不允许执行脚本，先执行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

激活成功后，终端前面通常会多一个 `(.venv)`。

#### 3. 安装依赖

```powershell
python -m pip install -U pip
pip install -r requirements.txt
```

#### 4. 创建数据库

这一步仍然可以在当前 PowerShell 里直接执行：

```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS blog_website CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
```

执行后会要求你输入 MySQL 的 root 密码。

#### 5. 生成 `.env`

如果项目里还没有 `.env`，执行：

```powershell
Copy-Item .env.example .env
```

#### 6. 修改 `.env`

打开 `D:\front\backend\.env`，把下面几项改成你的 MySQL 配置：

```env
DB_BACKEND=mysql
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的数据库密码
MYSQL_DATABASE=blog_website
```

#### 7. 启动后端

```powershell
python -m uvicorn app.main:app --reload
```

看到类似下面的日志就说明启动成功了：

```text
Uvicorn running on http://127.0.0.1:8000
Application startup complete.
```

### 方案 B：数据库命令在 MySQL 客户端执行，项目命令在 PowerShell 执行

适合下面这种情况：

- 你电脑装了 MySQL
- 但是 PowerShell 里输入 `mysql` 提示“不是内部或外部命令”

这时可以这样做：

#### 1. 仍然先在 PowerShell 里进入后端目录

```powershell
cd D:\front\backend
```

#### 2. 在 PowerShell 里完成虚拟环境和依赖安装

```powershell
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

#### 3. 打开 MySQL 自带客户端

可以使用这些方式之一：

- 开始菜单中的 `MySQL Command Line Client`
- 已配置好 `mysql.exe` 路径的 `cmd` 或 PowerShell

进入 MySQL 后执行：

```sql
CREATE DATABASE IF NOT EXISTS blog_website CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

#### 4. 回到 PowerShell，复制并修改 `.env`

```powershell
Copy-Item .env.example .env
```

然后修改：

```env
DB_BACKEND=mysql
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=你的数据库密码
MYSQL_DATABASE=blog_website
```

#### 5. 在 PowerShell 中启动后端

```powershell
python -m uvicorn app.main:app --reload
```

## 四、如果你只想先跑后端，不用数据库

如果你现在只是想先把后端跑起来，不想折腾 MySQL，可以直接用内存模式。

这时命令只需要在 `D:\front\backend` 执行：

```powershell
cd D:\front\backend
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

说明：

- 默认 `DB_BACKEND=memory`
- 这种方式不需要建数据库
- 但后端一重启，注册用户和文章数据会丢失

## 五、怎么判断命令该在哪执行

你可以用这个简单规则判断：

- 看到 `uvicorn`、`pip`、`python`、`Copy-Item` 这类命令：在 `D:\front\backend` 的 PowerShell 里执行
- 看到 `mysql -u root -p ...` 或 `CREATE DATABASE ...`：在 MySQL 相关终端里执行

## 六、常见报错

### 1. `mysql` 不是内部或外部命令

说明 PowerShell 找不到 MySQL 客户端。

解决办法：

- 用 `MySQL Command Line Client` 执行建库语句
- 或者把 MySQL 的 `bin` 目录加入 PATH

### 2. `Activate.ps1` 被禁止执行

先执行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

再执行：

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. 启动后打不开接口

先看终端有没有这句：

```text
Application startup complete.
```

然后访问：

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/api/v1/health`
- `http://127.0.0.1:8000/docs`

## 七、最短版命令清单

### MySQL 模式

在 `D:\front\backend` 的 PowerShell：

```powershell
cd D:\front\backend
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

把 `.env` 改成 MySQL 配置后，再执行：

```powershell
python -m uvicorn app.main:app --reload
```

在 MySQL 终端里执行：

```sql
CREATE DATABASE IF NOT EXISTS blog_website CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

### 内存模式

在 `D:\front\backend` 的 PowerShell：

```powershell
cd D:\front\backend
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```
