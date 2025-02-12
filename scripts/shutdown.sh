#!/bin/bash

# 使用 ps 命令查询包含 "gunicorn" 的进程，并获取它们的 PID
pids=$(ps aux | grep gunicorn | grep -v grep | awk '{print $2}')

# 检查是否找到 gunicorn 进程
if [ -n "$pids" ]; then
  # 遍历所有找到的 PID
  for pid in $pids; do
    # 使用 kill 命令关闭进程
    kill $pid
    echo "已关闭进程 PID: $pid"
  done
else
  echo "未找到 gunicorn 进程"
fi