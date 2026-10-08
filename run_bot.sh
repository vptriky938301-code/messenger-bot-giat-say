#!/usr/bin/env bash
# Khởi chạy Messenger Chatbot cho Page Bí Quyết Giặt Sấy Dân Sinh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="/Users/pc/Downloads/Học Marketing/Quản Lý Quảng Cáo cho Page   Giặt Sấy Dân Sinh/M5_App_Ads/.venv/bin/python3"

if [ -f "$PYTHON_BIN" ]; then
    echo "🚀 Đang khởi động Bot Giặt Sấy Dân Sinh với môi trường ảo Python..."
    "$PYTHON_BIN" auto_reply_bot.py
else
    echo "🚀 Đang khởi động Bot Giặt Sấy Dân Sinh với Python3 hệ thống..."
    python3 auto_reply_bot.py
fi
