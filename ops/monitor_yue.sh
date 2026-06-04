#!/bin/bash
# 简阅 - 容器与日志巡检脚本
CONTAINER="yue-app"
APP_URL="http://127.0.0.1:8000/health"

echo "==== 简阅运行监控 $(date '+%Y-%m-%d %H:%M:%S') ===="

echo "[1] 容器状态"
docker ps --filter "name=$CONTAINER"

echo -e "\n[2] 资源占用"
docker stats --no-stream "$CONTAINER"

echo -e "\n[3] 健康检查"
curl -s "$APP_URL" || echo "健康检查失败"

echo -e "\n[4] 最近 50 行日志"
docker logs --tail 50 "$CONTAINER"

echo -e "\n[5] 磁盘空间"
df -h

echo -e "\n巡检完成"
