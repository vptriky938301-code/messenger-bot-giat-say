"""
🤖 AUTO REPLY BOT — Page Bí Quyết Giặt Sấy Dân Sinh
Tự động trả lời tin nhắn Messenger + gửi link cẩm nang Giặt Xả

Tách riêng khỏi facebook_bot.py gốc để dễ quản lý.
"""

import os
import threading
import json
import time
import requests
import logging
import sys
from flask import Flask, request
from knowledge_base import find_topic, get_answer, get_fun_reply
from knowledge_deep import find_deep_topic
from ai_engine import ask_gemini

# Setup logging to file (tránh OSError khi terminal mất)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

def safe_print(msg):
    """Print an toàn — nếu terminal mất thì ghi log thay."""
    try:
        print(msg, flush=True)
    except OSError:
        logger.info(msg)

# ============================================
# CẤU HÌNH
# ============================================

# Đọc từ .env hoặc đặt trực tiếp
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "biquyetgiatsay_verify_2026")

# Chống trùng message (Facebook retry khi webhook chậm)
PROCESSED_MSGS = set()

# Link tài liệu (thay link thật vào đây hoặc trong .env)
LINK_CAM_NANG_NUOC_GIAT = os.environ.get(
    "LINK_CAM_NANG_NUOC_GIAT",
    "https://drive.google.com/your-link-nuoc-giat"
)
LINK_CAM_NANG_NUOC_XA = os.environ.get(
    "LINK_CAM_NANG_NUOC_XA",
    "https://drive.google.com/your-link-nuoc-xa"
)

API_URL = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

app = Flask(__name__)

# ============================================
# TIN NHẮN MẪU
# ============================================

# Tin chào mừng — Giọng Chuyên gia + Người Chăm sóc
MSG_CHAO_MUNG = (
    "Chào anh/chị! 👋\n\n"
    "Mình là Bí Quyết Giặt Sấy Dân Sinh — kênh chia sẻ kiến thức "
    "hoá chất giặt tẩy chuyên sâu, dành riêng cho anh chị chủ tiệm giặt.\n\n"
    "Mình có thể hỗ trợ anh/chị:\n"
    "🔬 Kiến thức hoá chất (nước giặt, nước xả, tẩy vết bẩn...)\n"
    "🔧 Mẹo vận hành máy giặt hiệu quả\n"
    "📊 Bảng định lượng tiết kiệm chi phí\n"
    "🏪 Kinh nghiệm vận hành tiệm giặt\n\n"
    "Hoặc gõ số để nhận tài liệu miễn phí:\n"
    "1️⃣ Cẩm nang Nước Giặt 2026 (30+ trang)\n"
    "2️⃣ Cẩm nang Nước Xả 2026 (20+ trang)\n"
    "3️⃣ Cả 2 bộ tài liệu\n\n"
    "Anh/chị cứ thoải mái hỏi, mình sẵn sàng hỗ trợ! 🙌"
)

# Tin gửi cẩm nang — Chân thành, tử tế, chia sẻ kiến thức free
MSG_GUI_NUOC_GIAT = (
    "📘 Cẩm nang Kiến thức Nước Giặt 2026 đây ạ!\n\n"
    f"👉 {LINK_CAM_NANG_NUOC_GIAT}\n\n"
    "Đây là bộ tài liệu mình tổng hợp từ 20 năm kinh nghiệm "
    "R&D hoá chất — viết riêng cho anh chị chủ tiệm giặt.\n\n"
    "Mình gợi ý đọc trước:\n"
    "• Chương 2 — Cơ chế tẩy rửa & 9 nhóm thành phần\n"
    "• Chương 4 — Cách đọc nhãn & định lượng đúng (tiết kiệm 18 triệu/năm)\n\n"
    "Đọc xong có thắc mắc gì cứ nhắn mình — mình giải đáp tận tình! 💪"
)

MSG_GUI_NUOC_XA = (
    "📗 Cẩm nang Kiến thức Nước Xả 2026 đây ạ!\n\n"
    f"👉 {LINK_CAM_NANG_NUOC_XA}\n\n"
    "Bộ tài liệu này giúp anh/chị hiểu rõ:\n"
    "• So sánh Quats vs Esterquats vs Silicone (chọn đúng = tiết kiệm + thơm lâu)\n"
    "• Bảng định lượng ml theo tải đồ\n"
    "• Công thức phối hợp giặt + xả chuẩn tiệm giặt\n\n"
    "Có gì chưa rõ cứ hỏi mình nha — mình giải thích dễ hiểu, "
    "không dùng từ hàn lâm khó hiểu đâu! 😊"
)

MSG_GUI_CA_HAI = (
    "📘📗 Trọn bộ 2 Cẩm nang Giặt Xả 2026 đây ạ!\n\n"
    f"1. Cẩm nang Nước Giặt: {LINK_CAM_NANG_NUOC_GIAT}\n"
    f"2. Cẩm nang Nước Xả: {LINK_CAM_NANG_NUOC_XA}\n\n"
    "Gợi ý đọc trước:\n"
    "• Nước Giặt → Chương 2 & 4 (công thức + định lượng)\n"
    "• Nước Xả → So sánh chất làm mềm & Bảng ml\n\n"
    "Tài liệu này mình chia sẻ miễn phí cho cộng đồng chủ tiệm giặt — "
    "vì mình tin kiến thức đúng sẽ giúp anh/chị tiết kiệm và nâng tầm dịch vụ! 💪\n\n"
    "Đọc xong nhắn mình, mình tư vấn thêm cho ạ!"
)

MSG_KHONG_HIEU = (
    "Cảm ơn anh/chị đã nhắn tin! 😊\n\n"
    "Mình có 2 bộ tài liệu miễn phí cho chủ tiệm giặt:\n"
    "1️⃣ Cẩm nang Nước Giặt\n"
    "2️⃣ Cẩm nang Nước Xả\n"
    "3️⃣ Cả 2 bộ\n\n"
    "Gõ số 1, 2 hoặc 3 để mình gửi link nhé!"
)

# Từ khóa nhận diện
KEYWORDS_CAM_NANG = ["cẩm nang", "tài liệu", "cam nang", "tai lieu", "pdf", "sách", "sach", "link", "gửi", "gui"]
KEYWORDS_NUOC_GIAT = ["nước giặt", "nuoc giat", "giặt"]
KEYWORDS_NUOC_XA = ["nước xả", "nuoc xa", "xả"]


# ============================================
# WEBHOOK HANDLERS
# ============================================

@app.route("/health", methods=["GET"])
def health():
    """Health check — Render và self-ping dùng endpoint này."""
    return "OK", 200

@app.route("/", methods=["GET"])
def verify():
    """Xác thực webhook với Facebook."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        safe_print("✅ Webhook verified!")
        return challenge, 200
    # Nếu không có params (truy cập trực tiếp) → trả 200 thay vì 403
    if not mode and not token:
        return "Bot is running 🤖", 200
    return "Forbidden", 403


def keep_alive():
    """Self-ping mỗi 14 phút — giữ Render free tier luôn thức."""
    url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url:
        return  # Chỉ chạy trên Render, không chạy local
    while True:
        time.sleep(840)  # 14 phút
        try:
            requests.get(f"{url}/health", timeout=10)
        except Exception:
            pass


@app.route("/", methods=["POST"])
def webhook():
    """Nhận và xử lý tin nhắn từ Messenger.
    Trả 200 NGAY → xử lý AI trong background thread."""
    data = request.get_json()

    if data.get("object") != "page":
        return "Not a page event", 404

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event["sender"]["id"]

            # Xử lý tin nhắn text
            if "message" in event and "text" in event["message"]:
                msg_id = event["message"].get("mid", "")
                # Chống trùng: skip nếu đã xử lý message này
                if msg_id in PROCESSED_MSGS:
                    safe_print(f"⏭️ Skip duplicate: {msg_id[-8:]}")
                    continue
                PROCESSED_MSGS.add(msg_id)
                # Giữ cache nhỏ
                if len(PROCESSED_MSGS) > 500:
                    PROCESSED_MSGS.clear()

                text = event["message"]["text"].strip().lower()
                safe_print(f"📩 Nhận: '{text}' từ {sender_id}")
                # Xử lý trong background thread → không block webhook
                threading.Thread(
                    target=handle_message,
                    args=(sender_id, text),
                    daemon=True
                ).start()

            # Xử lý postback (nút bấm)
            elif "postback" in event:
                payload = event["postback"].get("payload", "")
                handle_postback(sender_id, payload)

    return "OK", 200


# ============================================
# XỬ LÝ TIN NHẮN
# ============================================

def handle_message(sender_id, text):
    """Gõ 1/2/3 → gửi link. Mọi thứ khác → Gemini AI trả lời."""

    # Gõ số 1, 2, 3 → gửi link cẩm nang
    if text in ("1",):
        send_text(sender_id, MSG_GUI_NUOC_GIAT)
    elif text in ("2",):
        send_text(sender_id, MSG_GUI_NUOC_XA)
    elif text in ("3",):
        send_text(sender_id, MSG_GUI_CA_HAI)

    # 🤖 TẤT CẢ TIN NHẮN KHÁC → GEMINI AI
    else:
        ai_response = ask_gemini(text, sender_id=sender_id)
        # Retry 1 lần nếu rate limit
        if not ai_response:
            import time
            time.sleep(3)
            ai_response = ask_gemini(text, sender_id=sender_id)

        if ai_response:
            # Chia thành nhiều tin nhắn riêng (như người thật)
            parts = [p.strip() for p in ai_response.split("|||") if p.strip()]
            for i, part in enumerate(parts):
                send_text(sender_id, part)
                if i < len(parts) - 1:
                    import time
                    time.sleep(1)
        else:
            # Fallback ngắn gọn khi AI lỗi
            send_text(sender_id, "Anh/chị chờ mình xíu nha, mình đang bận tí 😊 Nhắn lại sau ít phút mình trả lời ngay ạ!")


def handle_postback(sender_id, payload):
    """Xử lý khi user bấm nút."""
    if payload == "GET_NUOC_GIAT":
        send_text(sender_id, MSG_GUI_NUOC_GIAT)
    elif payload == "GET_NUOC_XA":
        send_text(sender_id, MSG_GUI_NUOC_XA)
    elif payload == "GET_CA_HAI":
        send_text(sender_id, MSG_GUI_CA_HAI)
    else:
        send_text(sender_id, MSG_CHAO_MUNG)


# ============================================
# GỬI TIN NHẮN
# ============================================

def send_text(recipient_id, text):
    """Gửi tin nhắn text đến user."""
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        safe_print(f"✅ Sent to {recipient_id}")
    else:
        safe_print(f"❌ Error {response.status_code}: {response.text}")
    return response


def send_buttons(recipient_id, text, buttons):
    """Gửi tin nhắn có nút bấm."""
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }
        },
        "messaging_type": "RESPONSE"
    }
    response = requests.post(API_URL, json=payload)
    return response


# ============================================
# CHẠY
# ============================================

if __name__ == "__main__":
    # Load .env nếu có
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

        # Reload config sau khi đọc .env
        PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
        VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "biquyetgiatsay_verify_2026")
        LINK_CAM_NANG_NUOC_GIAT = os.environ.get("LINK_CAM_NANG_NUOC_GIAT", "")
        LINK_CAM_NANG_NUOC_XA = os.environ.get("LINK_CAM_NANG_NUOC_XA", "")

        # Cập nhật API URL và tin nhắn
        globals()["API_URL"] = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
        globals()["MSG_GUI_NUOC_GIAT"] = (
            "📘 Đây là link Cẩm nang Kiến thức Nước Giặt 2026:\n\n"
            f"👉 {LINK_CAM_NANG_NUOC_GIAT}\n\n"
            "Mình gợi ý bạn đọc trước:\n"
            "• Chương 2 — Cơ chế tẩy rửa & 9 nhóm thành phần\n"
            "• Chương 4 — Cách đọc nhãn & định lượng đúng\n\n"
            "Có thắc mắc gì cứ nhắn mình nhé! 🙌"
        )
        globals()["MSG_GUI_NUOC_XA"] = (
            "📗 Đây là link Cẩm nang Kiến thức Nước Xả 2026:\n\n"
            f"👉 {LINK_CAM_NANG_NUOC_XA}\n\n"
            "Mình gợi ý bạn đọc trước:\n"
            "• Phần so sánh 3 nhóm chất làm mềm (Quats vs Esterquats vs Silicone)\n"
            "• Bảng định lượng ml theo tải đồ\n\n"
            "Có thắc mắc gì cứ nhắn mình nhé! 🙌"
        )
        globals()["MSG_GUI_CA_HAI"] = (
            "📘📗 Đây là link cả 2 bộ Cẩm nang Giặt Xả 2026:\n\n"
            f"1. Nước Giặt: {LINK_CAM_NANG_NUOC_GIAT}\n"
            f"2. Nước Xả: {LINK_CAM_NANG_NUOC_XA}\n\n"
            "Gợi ý đọc trước:\n"
            "• Nước Giặt → Chương 2 & 4\n"
            "• Nước Xả → So sánh chất làm mềm & Bảng ml\n\n"
            "Chúc bạn áp dụng hiệu quả cho tiệm! 💪"
        )

    if not PAGE_ACCESS_TOKEN:
        safe_print("❌ Thiếu PAGE_ACCESS_TOKEN! Kiểm tra file .env")
        exit(1)

    safe_print("🤖 Bot Bí Quyết Giặt Sấy Dân Sinh đang chạy...")
    safe_print(f"   Token: ...{PAGE_ACCESS_TOKEN[-10:]}")
    safe_print(f"   Verify: {VERIFY_TOKEN}")

    # Giữ Render free tier luôn thức
    threading.Thread(target=keep_alive, daemon=True).start()

    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=(port == 8000))
