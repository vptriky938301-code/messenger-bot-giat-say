"""
🤖 AI Engine — Gemini-powered Chatbot Tư Vấn Giải Pháp Quà Tặng Doanh Nghiệp
Hỗ trợ tư vấn theo ngân sách (50k - 300k+), set quà công đoàn/Tết, in logo, xuất VAT, gửi mẫu thử và chốt SĐT.
"""
import os
import json
from dotenv import load_dotenv
from google import genai
from knowledge_base import BRAND_INFO, GIFT_PACKAGES, PRODUCTS, B2B_POLICIES

load_dotenv()

# ============================================
# GEMINI CLIENT
# ============================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print(f"✅ Gemini AI đã kết nối thành công (key: ...{GEMINI_API_KEY[-6:]})")
    except Exception as e:
        print(f"⚠️ Lỗi khởi tạo Gemini Client: {e}")
else:
    print("⚠️ Chưa có GEMINI_API_KEY — bot sẽ chạy chế độ rule/keyword")

# ============================================
# QUẢN LÝ LỊCH SỬ CHAT (IN-MEMORY HISTORY)
# ============================================
CHAT_HISTORIES = {}
MAX_HISTORY_TURNS = 10

def _add_to_history(sender_id, role, text):
    """Lưu tin nhắn vào lịch sử phiên chat."""
    if sender_id not in CHAT_HISTORIES:
        CHAT_HISTORIES[sender_id] = []
    CHAT_HISTORIES[sender_id].append({"role": role, "text": text})
    if len(CHAT_HISTORIES[sender_id]) > MAX_HISTORY_TURNS * 2:
        CHAT_HISTORIES[sender_id] = CHAT_HISTORIES[sender_id][-MAX_HISTORY_TURNS * 2:]

def _build_contents(sender_id, user_message):
    """Chuyển lịch sử chat thành format genai."""
    history = CHAT_HISTORIES.get(sender_id, [])
    if not history:
        return user_message
    contents = []
    for turn in history:
        contents.append(genai.types.Content(
            role=turn["role"],
            parts=[genai.types.Part(text=turn["text"])]
        ))
    contents.append(genai.types.Content(
        role="user",
        parts=[genai.types.Part(text=user_message)]
    ))
    return contents

# ============================================
# SYSTEM PROMPT — TRỢ LÝ QUÀ TẶNG DOANH NGHIỆP
# ============================================
SYSTEM_PROMPT = f"""Bạn là Chuyên viên tư vấn giải pháp của Page "Giải Pháp Quà Tặng Doanh Nghiệp" (thuộc Bách Hóa Sạch 2S).
Bạn đang chat trực tiếp với khách hàng là các đại diện doanh nghiệp: Trưởng phòng Hành chính Nhân sự (HR), Chủ tịch Công đoàn, Ban trù bị mua sắm hoặc Giám đốc doanh nghiệp.

=== THÔNG TIN THƯƠNG HIỆU & ĐỊNH VỊ ===
- Đơn vị: Bách Hóa Sạch 2S — hơn 20 năm kinh nghiệm sản xuất hóa mỹ phẩm tiêu dùng.
- Sứ mệnh: Mang đến bộ quà tặng tiêu dùng THIẾT THỰC (Nước giặt Lozzi, Lau sàn Caro, Rửa chén Caro, Rửa tay Carose).
- Triết lý quà tặng: "100% người nhận đều sử dụng được hàng ngày — Không lãng phí — Tối ưu chi phí doanh nghiệp".

=== CÁC GÓI QUÀ TẶNG THEO PHÂN KHÚC NGÂN SÁCH ===
{json.dumps(GIFT_PACKAGES, ensure_ascii=False, indent=2)}

=== THÔNG TIN SẢN PHẨM ===
{json.dumps(PRODUCTS, ensure_ascii=False, indent=2)}

=== CHÍNH SÁCH B2B DOANH NGHIỆP QUAN TRỌNG ===
{json.dumps(B2B_POLICIES, ensure_ascii=False, indent=2)}

=== PHONG CÁCH TƯ VẤN ===
1. Tác phong: Chuyên nghiệp, chu đáo, nhiệt tình, lịch sự, thấu hiểu áp lực cân đối ngân sách của người làm quà tặng công ty.
2. Xưng hô: Xưng "em" hoặc "mình", gọi khách là "anh/chị".
3. Cách nhắn tin:
   - Dùng ký hiệu ||| để ngăn cách các tin nhắn ngắn (tạo cảm giác người thật đang gõ chat tự nhiên).
   - Mỗi lượt chỉ gửi 2-3 tin ngắn, không viết văn bản dài dòng như tiểu luận.
   - Nhắn từng ý rõ ràng, súc tích.
4. Điều hướng nhu cầu thông minh:
   - Khi khách hỏi quà tặng → Khéo léo hỏi số lượng nhân sự dự kiến và mức ngân sách/suất (ví dụ: 80k, 100k, 150k hay 200k+).
   - Gợi ý ngay set quà phù hợp nhất từ xưởng.
   - Nhấn mạnh các cam kết an tâm cho doanh nghiệp: Đầy đủ hóa đơn đỏ VAT, Hợp đồng kinh tế, miễn phí in logo doanh nghiệp lên set quà, và ĐẶC BIỆT là gửi bộ mẫu thật (Sample Kit) miễn phí tận công ty để duyệt trước.
5. Chốt Lead (Số điện thoại / Zalo):
   - Khi đã tư vấn cơ bản, hãy lịch sự xin Số điện thoại/Zalo hoặc Email để gửi Bảng báo giá chiết khấu cụ thể theo số lượng + File Catalog PDF chất lượng cao.
"""

def ask_gemini(user_message, sender_id=None):
    """Gọi Gemini AI với lịch sử hội thoại."""
    if not client:
        return None
    
    contents = _build_contents(sender_id, user_message) if sender_id else user_message
    
    models = ["gemini-3.1-flash-lite", "gemini-3.8-flash", "gemini-2.5-flash"]
    
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=1024,
                )
            )
            answer = response.text.strip() if response.text else None
            if answer:
                if sender_id:
                    _add_to_history(sender_id, "user", user_message)
                    _add_to_history(sender_id, "model", answer)
                return answer
        except Exception as e:
            print(f"⚠️ Thử model {model_name} thất bại: {e}")
            continue
            
    return None
