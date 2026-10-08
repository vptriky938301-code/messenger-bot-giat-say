"""
🤖 AUTO REPLY BOT — Page Giải Pháp Quà Tặng Doanh Nghiệp (Bách Hóa Sạch 2S)
Tự động tư vấn giải pháp quà tặng B2B, set quà Tết, công đoàn, xuất VAT, gửi mẫu và chốt số điện thoại.
"""

import os
import re
import sys
import json
import time
import logging
import threading
import requests
from datetime import datetime
from flask import Flask, request
from dotenv import load_dotenv

# Nạp biến môi trường từ .env
load_dotenv()

# Import module AI và Knowledge
from knowledge_base import find_quatang_topic, GIFT_PACKAGES, BRAND_INFO
from ai_engine import ask_gemini

# ============================================
# CẤU HÌNH LOGGING
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# CẤU HÌNH BIẾN MÔI TRƯỜNG
# ============================================
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "bhs_quatang_verify_2026")
PORT = int(os.environ.get("PORT", 5001))
LINK_CATALOG = os.environ.get("LINK_CATALOG_QUA_TANG", "https://example.com/catalog-qua-tang-bhs2s-2026.pdf")

API_MESSAGES_URL = f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

# File lưu Lead khách hàng để lại SĐT
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
LEADS_FILE = os.path.join(DATA_DIR, "leads_quatang.json")

# Chống xử lý trùng tin nhắn Facebook
PROCESSED_MESSAGES = set()

app = Flask(__name__)

# ============================================
# CÁC MẪU TIN NHẮN CHUẨN B2B
# ============================================
MSG_WELCOME = (
    "Dạ em chào anh/chị! 👋\n\n"
    "Em là trợ lý tư vấn của Page **Giải Pháp Quà Tặng Doanh Nghiệp** (thuộc Bách Hóa Sạch 2S).\n\n"
    "Bên em chuyên cung cấp các set quà tặng tiêu dùng thiết thực (Nước giặt Lozzi, Lau sàn Caro, Rửa chén Caro, Rửa tay Carose) "
    "dành riêng cho Công đoàn, Công ty xí nghiệp, Nhà máy với mức chiết khấu tận xưởng và đầy đủ hóa đơn đỏ VAT.\n\n"
    "Em có thể hỗ trợ anh/chị:\n"
    "1️⃣ Tư vấn set quà theo ngân sách (50k - 100k - 150k - 200k+)\n"
    "2️⃣ Nhận trọn bộ Catalog & Báo giá chiết khấu doanh nghiệp\n"
    "3️⃣ Đăng ký nhận Hộp mẫu thực tế (Sample Kit) miễn phí tận công ty\n"
    "4️⃣ Tư vấn in logo thương hiệu & xuất hóa đơn VAT\n\n"
    "Anh/chị đang dự kiến ngân sách bao nhiêu cho mỗi suất quà, hoặc công ty mình có khoảng bao nhiêu nhân sự vậy ạ?"
)

# ============================================
# HÀM GỬI TIN NHẮN FACEBOOK API
# ============================================
def send_action(sender_id, action="typing_on"):
    """Gửi trạng thái 'đang nhập' hoặc 'đã xem'."""
    try:
        requests.post(
            API_MESSAGES_URL,
            json={"recipient": {"id": sender_id}, "sender_action": action},
            timeout=5
        )
    except Exception as e:
        logger.error(f"Lỗi send_action {action}: {e}")

def send_text_message(sender_id, text):
    """Gửi một tin nhắn văn bản."""
    if not text:
        return
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": text}
    }
    try:
        res = requests.post(API_MESSAGES_URL, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        logger.error(f"Lỗi send_text_message: {e}")
        return None

def send_quick_replies(sender_id, text, quick_replies):
    """Gửi tin nhắn kèm các nút bấm nhanh (Quick Replies)."""
    payload = {
        "recipient": {"id": sender_id},
        "message": {
            "text": text,
            "quick_replies": quick_replies
        }
    }
    try:
        res = requests.post(API_MESSAGES_URL, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        logger.error(f"Lỗi send_quick_replies: {e}")
        return None

def save_lead(sender_id, phone, note=""):
    """Lưu số điện thoại của khách vào file JSON để đội ngũ Sale chăm sóc."""
    leads = []
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                leads = json.load(f)
        except Exception:
            leads = []
            
    lead_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sender_id": sender_id,
        "phone": phone,
        "note": note,
        "status": "NEW"
    }
    leads.append(lead_entry)
    
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    logger.info(f"🎯 ĐÃ LƯU LEAD MỚI: SĐT {phone} (ID: {sender_id})")

def extract_phone_number(text):
    """Trích xuất số điện thoại Việt Nam từ văn bản."""
    pattern = r'(?:0|\+84)(?:3|5|7|8|9)\d{8}\b'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    # Tìm chuỗi 10 chữ số bắt đầu bằng 0
    pattern_alt = r'\b0\d{9}\b'
    match_alt = re.search(pattern_alt, text)
    return match_alt.group(0) if match_alt else None

# ============================================
# XỬ LÝ NỘI DUNG TIN NHẮN (BACKGROUND THREAD)
# ============================================
def process_message_async(sender_id, message_text):
    """Xử lý hội thoại tự động trong thread riêng biệt."""
    send_action(sender_id, "mark_seen")
    send_action(sender_id, "typing_on")
    time.sleep(0.8)
    
    clean_text = message_text.strip()
    
    # 1. KIỂM TRA KHÁCH CÓ GỬI SỐ ĐIỆN THOẠI KHÔNG
    phone = extract_phone_number(clean_text)
    if phone:
        save_lead(sender_id, phone, note=clean_text)
        confirm_msg = (
            f"Dạ em đã nhận được số điện thoại **{phone}** của anh/chị rồi ạ! 🎉|||"
            "Chuyên viên phụ trách giải pháp quà tặng doanh nghiệp bên em sẽ chủ động kết nối Zalo/điện thoại ngay trong ít phút tới "
            "để gửi Bảng báo giá chiết khấu chi tiết và hỗ trợ gửi mẫu tận nơi cho anh/chị nhé ạ! 🙏✨"
        )
        for part in confirm_msg.split("|||"):
            send_text_message(sender_id, part.strip())
            time.sleep(1.2)
        return

    # 2. XỬ LÝ QUICK REPLIES HOẶC TỪ KHÓA B2B
    topic = find_quatang_topic(clean_text)
    
    if topic == "catalog":
        msg = (
            f"Dạ em gửi anh/chị link xem và tải file **Catalog Quà Tặng Doanh Nghiệp 2026** đầy đủ các set tại đây ạ:\n\n"
            f"👉 {LINK_CATALOG}\n\n"
            "Anh/chị xem qua và ưng ý set nào hoặc muốn điều chỉnh món theo ngân sách công ty thì nhắn em nhé! "
            "Anh/chị có thể để lại SĐT/Zalo để em gửi kèm bảng chiết khấu theo số lượng ạ. 😊"
        )
        send_text_message(sender_id, msg)
        return

    if topic == "mau_thu":
        msg = (
            "Dạ bên em có chính sách **GỬI BỘ MẪU THẬT (SAMPLE KIT) MIỄN PHÍ** tận văn phòng công ty cho ban trù bị hoặc công đoàn duyệt trực tiếp trước khi đặt ạ! 📦✨|||"
            "Anh/chị chỉ cần để lại Số điện thoại + Tên công ty và địa chỉ, bên em sẽ chuẩn bị mẫu gửi đến tận nơi cho mình ngay trong 1-2 ngày tới nha!"
        )
        for part in msg.split("|||"):
            send_text_message(sender_id, part.strip())
            time.sleep(1.2)
        return

    if topic == "vat_hop_dong":
        msg = (
            "Dạ anh/chị hoàn toàn yên tâm ạ! Bách Hóa Sạch 2S là đơn vị sản xuất trực tiếp:|||"
            "✅ Xuất đầy đủ Hóa đơn đỏ GTGT (VAT) điện tử hợp pháp cho doanh nghiệp\n"
            "✅ Hợp đồng kinh tế và biên bản giao nhận minh bạch\n"
            "✅ Đầy đủ kiểm định chất lượng xuất xưởng|||"
            "Anh/chị cần báo giá trước hay cần làm hợp đồng mẫu thì để lại SĐT bên em gửi thủ tục qua Zalo/Email cho kế toán mình duyệt nha!"
        )
        for part in msg.split("|||"):
            send_text_message(sender_id, part.strip())
            time.sleep(1.2)
        return

    # 3. GỌI GEMINI AI NẾU KHÔNG TRÚNG RULE CỨNG
    ai_reply = ask_gemini(clean_text, sender_id=sender_id)
    
    if ai_reply:
        parts = [p.strip() for p in ai_reply.split("|||") if p.strip()]
        for p in parts:
            send_text_message(sender_id, p)
            time.sleep(1.2)
    else:
        # Fallback tin nhắn chào mừng chuẩn
        send_text_message(sender_id, MSG_WELCOME)

# ============================================
# FLASK WEBHOOK ROUTES
# ============================================
@app.route("/", methods=["GET"])
@app.route("/webhook", methods=["GET"])
def verify():
    """Facebook Webhook verification."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("✅ Facebook Webhook đã được xác thực thành công!")
        return challenge, 200
    else:
        logger.warning(f"❌ Xác thực Webhook thất bại: token nhận được '{token}' != '{VERIFY_TOKEN}'")
        return "Verification token mismatch", 403

@app.route("/", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def webhook():
    """Xử lý nhận tin nhắn từ Facebook Messenger."""
    data = request.get_json()
    if not data or data.get("object") != "page":
        return "EVENT_RECEIVED", 200

    for entry in data.get("entry", []):
        for messaging_event in entry.get("messaging", []):
            sender_id = messaging_event.get("sender", {}).get("id")
            
            # Khách gửi tin nhắn text
            if "message" in messaging_event:
                msg = messaging_event["message"]
                mid = msg.get("mid")
                text = msg.get("text")
                quick_reply = msg.get("quick_reply", {}).get("payload")
                
                # Tránh lặp tin
                if mid and mid in PROCESSED_MESSAGES:
                    continue
                if mid:
                    PROCESSED_MESSAGES.add(mid)
                    if len(PROCESSED_MESSAGES) > 1000:
                        PROCESSED_MESSAGES.clear()

                actual_text = quick_reply or text
                if sender_id and actual_text:
                    logger.info(f"📩 Nhận tin từ {sender_id}: {actual_text}")
                    # Xử lý async trong background thread
                    t = threading.Thread(target=process_message_async, args=(sender_id, actual_text))
                    t.daemon = True
                    t.start()
                    
            # Khách bấm Postback Button (ví dụ Get Started)
            elif "postback" in messaging_event:
                payload = messaging_event["postback"].get("payload")
                logger.info(f"🔘 Postback từ {sender_id}: {payload}")
                t = threading.Thread(target=process_message_async, args=(sender_id, "báo giá"))
                t.daemon = True
                t.start()

    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    print(f"🚀 Bot Quà Tặng Doanh Nghiệp đang chạy tại cổng http://localhost:{PORT}")
    print(f"🔗 Webhook Verify Token: {VERIFY_TOKEN}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
