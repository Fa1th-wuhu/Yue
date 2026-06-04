#!/bin/bash
set -e
# 简阅 - 一键部署（适配 GitHub 拉取不稳场景）
ZIP_FILE="/root/Yue.zip"
APP_DIR="/root/Yue"

if [ ! -f "$ZIP_FILE" ]; then
  echo "未找到部署包: $ZIP_FILE (请先 scp 上传 Yue.zip)"
  exit 1
fi

echo "开始部署..."

# 若已有运行容器，先停止
test -d "$APP_DIR" && { cd "$APP_DIR" && docker-compose down || true; }

rm -rf "$APP_DIR"
unzip -o "$ZIP_FILE" -d "$APP_DIR"
cd "$APP_DIR"

# 兼容旧版 docker-compose，需要 version 行
if ! head -n 1 docker-compose.yml | grep -q "version"; then
  sed -i '1i version: "3.7"' docker-compose.yml
fi

# 修改前端 API 地址为当前云机 IP（可按需调整）
sed -i 's#http://127.0.0.1:8000/api#http://10.42.78.219:8000/api#g' code_artifact.html

# 启动
docker-compose up -d --build

echo "部署完成"
docker ps
curl -s http://127.0.0.1:8000/health || true
