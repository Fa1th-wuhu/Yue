#!/bin/bash
# 简阅 - 容器与日志巡检脚本
CONTAINER="yue-app"
APP_URL="http://127.0.0.1:8000/health"

echo "==== 简阅运行监控 $(date '+%Y-%m-%d %H:%M:%S') ===="

echo "[1] 容器状态"
docker ps --filter "name=$CONTAINER"

echo -e "\n[2] 资源占用"
docker stats --no-stream "$CONTAINER"

echo -e "\n[3] 健康检查与监控自愈"
if curl -s -f "$APP_URL" > /dev/null; then
    echo "健康检查成功：后端服务正常响应中 (OK)"
else
    echo "⚠️ 警告：检测到后端服务故障或未启动！"
    echo "⚙️ 启动自动修复机制：正在尝试自动重启容器 $CONTAINER..."
    docker restart "$CONTAINER"
    echo "正在等待服务唤醒..."
    sleep 3
    if curl -s -f "$APP_URL" > /dev/null; then
        echo "✅ [自愈成功] 容器已自动拉起，服务已恢复正常运行！"
    else
        echo "❌ [自愈失败] 无法通过自动重启恢复，请立即执行人工排查或使用 /root/Yue/ops/restore_yue_db.sh 恢复数据库。"
    fi
fi

echo -e "\n[4] 最近 50 行日志"
docker logs --tail 50 "$CONTAINER"

echo -e "\n[5] 磁盘空间"
df -h

echo -e "\n巡检完成"
