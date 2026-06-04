#!/bin/bash
set -e
# 简阅 - 代码与数据库备份
APP_DIR="/root/Yue"
BACKUP_DIR="/root/backups/yue"
CONTAINER="yue-app"
TIME=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/yue_project_$TIME.tar.gz"
DB_BACKUP="$BACKUP_DIR/yue_$TIME.db"

mkdir -p "$BACKUP_DIR"

echo "开始备份..."

# 备份数据库（数据卷）
docker cp "$CONTAINER":/app/data/yue.db "$DB_BACKUP" || echo "WARN: 无法从容器拷贝 yue.db"

# 备份代码与配置
tar -czf "$BACKUP_FILE" \
  -C "$APP_DIR" \
  code_artifact.html \
  docker-compose.yml \
  Dockerfile \
  backend \
  add_santi.py 2>/dev/null || true

echo "备份完成：$BACKUP_FILE"
echo "数据库备份：$DB_BACKUP"

# 清理 7 天前的旧备份
find "$BACKUP_DIR" -type f -mtime +7 -delete || true
