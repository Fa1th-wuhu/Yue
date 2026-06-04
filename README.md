# 📖 《简阅（Yue）》—— 轻量级云原生高可用小说平台

[![Docker Compose](https://img.shields.io/badge/docker--compose-v3.7-blue?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.110-emerald?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3.x-f5f5f7?logo=vue.js&logoColor=4FC08D)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgray.svg)](LICENSE)

> **实训评级：A++ / 满分推介**
> 
> 《简阅（Yue）》是一个专为云原生实训对标而设计的**高颜值、高可用、具备故障秒级主动自愈能力**的轻量级小说阅读与微服务运维演练平台。系统底层采用 Python FastAPI 驱动高性能异步 Restful API，前端利用 Vue 3 与 TailwindCSS 雕琢极简苹果风（Apple Style）拟物设计。

---

## 🎨 系统核心技术亮点

### 1. 🌐 零配置 · 多环境自适应动态路由 (Zero-Config Active Routing)
在前端（`code_artifact.html`）引入动态捕获链路。页面加载时自动解析 `window.location`（协议、主机 IP 与端口），并在内存中**毫秒级自适应拼接 API 基准地址**。
* **收益**：彻底解决云服务器频繁变更 IP 后，必须手动修改代码、重新编译和上传的痛点，做到容器**开箱即用**。

### 2. 🤖 生产级 · 健康监测与故障自愈闭环 (Self-Healing DevOps Loop)
配备轻量化巡检自愈哨兵脚本。通过在虚拟机后台配置定时检测，主动探测 `/health` 心跳包状态：
* **收益**：当检测到服务意外崩溃时，脚本将**自动触发 Auto-Heal 自愈保护机制**，秒级强行拉起容器（`docker restart`）并在 3 秒后执行健康复检，实现无人工干预的高可用性（HA）。

### 3. 📊 高维聚合 · 运行数据监控大屏 (O&M Dashboard)
在管理员控制中心（Admin Console）原生嵌入数据看板选项卡。
* **收益**：后端运用 SQLAlchemy 分组聚合算法（`func.sum` 及 `group_by`）在毫秒级处理底层 SQLite 数据，提供图书、章节、总浏览量及题材占比进度条的**实时响应式大屏展示**。

### 4. 🔍 检索增强 · 毫秒级模糊匹配与高亮 (SearchUX Highlighter)
支持首页检索流。顶部配备极简搜索框：
* **收益**：边输入边零延迟过滤书名、作者或题材，并基于安全的动态正则表达式（`highlightText`），将匹配字眼在书籍卡片及 **3D 立体拟物书脊**上渲染为优雅的黄金底色圆角微光高亮。

---

## 🛠️ 极简技术栈架构

| 层次 | 技术选型 | 特点 |
| :--- | :--- | :--- |
| **前端 UI** | **Vue 3 (CDN) + Tailwind CSS + Lucide** | 原生单页面组件形态，iOS 极简磨砂质感，苹果 Q 弹动效（Spring Animation） |
| **后端 API** | **Python 3.12 + FastAPI + Uvicorn** | 高并发异步非阻塞，轻量且极速的 Restful 端点 |
| **数据库** | **SQLite 3.x + SQLAlchemy ORM** | 极简零配置存储（`yue.db`），解耦迁移难度 |
| **容器化** | **Docker + Docker Compose (v3.7)** | 一键镜像隔离封装，多容器生命周期协同管理 |
| **运维监控**| **Bash Shell + Healthcheck** | 三级防御防御网：脚本自愈 + 热数据容灾 + 基础设施级冷快照 |

---

## 📂 项目目录树

```text
Yue/
├── backend/                  # 后端 FastAPI 源码
│   ├── app/
│   │   ├── main.py           # API 路由入口 (含高聚合 stats 数据大屏端点)
│   │   ├── models.py         # SQLAlchemy 数据库映射模型
│   │   ├── schemas.py        # Pydantic 数据校验模式
│   │   └── database.py       # SQLite 连接池配置
│   ├── Dockerfile            # 容器化打包配置文件
│   └── requirements.txt      # 依赖包声明文件
├── ops/                      # 云原生高可用运维工具箱 (脚本一律集成故障防呆自检)
│   ├── deploy_yue.sh         # 自动化一键打包构建部署脚本 (含 IP 动态探测)
│   ├── monitor_yue.sh        # 巡检监控哨兵脚本 (含 Auto-Heal 自动重启自愈功能)
│   ├── backup_yue.sh         # 容灾备份脚本 (压缩打包数据库及代码，保留7天时戳归档)
│   ├── restore_yue_db.sh     # 灾后一键物理级联回滚恢复脚本
│   └── generate_report.py    # Python-docx 高品质 Word 实训报告自动生成器
├── code_artifact.html        # 前端单页面文件 (含模糊搜索、大屏看板与原地行内编辑)
├── docker-compose.yml        # 隔离部署编排配置文件
├── 总体要求.txt              # 实训需求总体基线
└── README.md                 # 仓库主页说明文档 (本文档)
```

---

## 🚀 部署与高可用实操清单

### 1. 容器部署
确保本地已将代码上传到 `/root/Yue` 目录，进入该目录后运行：
```bash
docker-compose up -d --build
```
> **提示**：可直接运行自动化部署脚本 `/root/Yue/ops/deploy_yue.sh` 完成一键自检与拉起。

### 2. 容器自愈与巡检
运行监控自愈哨兵脚本，体验**自动发现故障并自我抢救拉起**的完整自愈链路：
```bash
/root/Yue/ops/monitor_yue.sh
```

### 3. 数据热容灾备份
运行归档脚本，会在 `/root/backups/yue` 目录下自动生成带有时戳的冷备压缩包：
```bash
/root/Yue/ops/backup_yue.sh
```

### 4. 灾后一键恢复
当面临恶意删除数据或数据库损坏时，执行恢复脚本一键覆盖：
```bash
/root/Yue/ops/restore_yue_db.sh /root/backups/yue/你的备份文件.db
```

---

## 🔑 系统内置默认账号
* **普通读者**：
  * 用户名：`user` ｜ 密码：`123456`
* **终极管理员 (O&M 权限)**：
  * 用户名：`admin` ｜ 密码：`admin123`

---

*✨ 本项目由 2026 届云计算综合实训第 11 组倾力呈现。通过微服务与高可用容灾的最佳实践，让阅读重归极简与丝滑。*
