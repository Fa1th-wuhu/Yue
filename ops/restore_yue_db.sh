#!/bin/bash
set -e
# 简阅 - 数据库恢复
if [ -z "$1" ]; then
  echo "用法: ./restore_yue_db.sh /root/backups/yue/yue_XXXX.db"
  exit 1
fi
DB_FILE="$1"
CONTAINER="yue-app"

if [ ! -f "$DB_FILE" ]; then
  echo "备份文件不存在: $DB_FILE"
  exit 1
fi

echo "恢复数据库: $DB_FILE"

docker-compose down || true
docker-compose up -d
sleep 3
docker cp "$DB_FILE" "$CONTAINER":/app/data/yue.db
docker restart "$CONTAINER"
echo "恢复完成，容器已重启"
