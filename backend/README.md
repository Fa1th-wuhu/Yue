# 简阅后端 API

这是根据 `code_artifact.html` 前端实现的 FastAPI 后端，接口路径与前端 `API_BASE_URL` 调用保持一致。

## 本地启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

启动后访问：

- 前端页面：http://127.0.0.1:8000/
- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/health

## 前端联调

将 `code_artifact.html` 中：

```js
const USE_MOCK = true;
```

改为：

```js
const USE_MOCK = false;
```

默认接口地址已是：

```js
const API_BASE_URL = "http://127.0.0.1:8000/api";
```

## 默认账号

- 管理员：admin / 123456
- 普通用户：user1 / 123456

## Docker 部署

在项目根目录执行：

```powershell
docker compose up -d --build
```

云服务器安全组需要开放 `8000` 端口，或通过 Nginx 反向代理到 `8000`。

## 已实现接口

- `POST /api/users/login`
- `POST /api/users/register`
- `GET /api/books`
- `POST /api/books`
- `PUT /api/books/{book_id}`
- `POST /api/books/{book_id}/like`
- `GET /api/chapters`
- `POST /api/chapters`
- `PUT /api/chapters/{chapter_id}`
- `GET /api/bookshelf`
- `POST /api/bookshelf`
- `DELETE /api/bookshelf/{item_id}`
- `GET /api/comments`
- `POST /api/comments`
- `GET /api/categories`
- `POST /api/categories`
- `DELETE /api/categories/{cat_name}`

## 数据持久化

默认使用 SQLite，数据库文件位于 `backend/data/yue.db` 或 Docker 卷 `/app/data/yue.db`。后期如需迁移 MySQL/PostgreSQL，可通过环境变量 `DATABASE_URL` 切换。
