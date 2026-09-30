"""
🤖 AI Engine — Gemini-powered chatbot chuyên gia hoá chất giặt là
Nạp toàn bộ 2 Cẩm nang (200KB) + Brand DNA BHS 2S làm nguyên liệu chính
Model: gemini-2.5-flash
"""
import os
from google import genai

# ============================================
# GEMINI CLIENT
# ============================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print(f"✅ Gemini AI đã kết nối (key: ...{GEMINI_API_KEY[-6:]})")
else:
    print("⚠️ Chưa có GEMINI_API_KEY — bot chạy chế độ keyword")

# ============================================
# NẠP DỮ LIỆU TỪ 2 CẨM NANG
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_guidebook(filename):
    """Đọc toàn bộ nội dung cẩm nang."""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"📚 Đã nạp: {filename} ({len(content):,} ký tự)")
        return content
    except FileNotFoundError:
        print(f"⚠️ Không tìm thấy: {filepath}")
        return ""

# Nạp 2 cẩm nang hoàn chỉnh
CAM_NANG_NUOC_GIAT = load_guidebook("CAM_NANG_NUOC_GIAT_HOAN_CHINH.md")
CAM_NANG_NUOC_XA = load_guidebook("Cam_nang_nuoc_xa_vai.md")

# ============================================
# SYSTEM PROMPT — "BỘ NÃO" CỦA BOT
# ============================================
SYSTEM_PROMPT = f"""Bạn là "Bí Quyết Giặt Sấy Dân Sinh" — chuyên gia tư vấn hoá chất giặt là số 1 Việt Nam trên Facebook Messenger.

=== THÔNG TIN KÊNH ===
- Kênh: Page Facebook "Bí Quyết Giặt Sấy Dân Sinh" (page lạnh, kênh chia sẻ kiến thức chuyên sâu)
- Thương hiệu gốc: Bách Hoá Sạch 2S (BHS 2S)
- Sản phẩm: LOZZI (nước giặt), CARO (nước lau sàn), MoveX (tẩy rửa), DEFA (đa năng)
- Khách hàng: Chủ tiệm giặt là dân sinh tại Việt Nam
- Người sáng lập: Kỹ sư Hoá học Nguyễn Thị Hải Yến — 20 năm kinh nghiệm R&D

=== BRAND DNA — TUÂN THỦ BẮT BUỘC ===
HÌNH MẪU: Chuyên gia (kiến thức chuyên sâu, bằng chứng khoa học) + Người Chăm sóc (đồng cảm, nhẹ nhàng, chia sẻ)
TÍNH CÁCH: Đam mê, Chân thành, Tử tế
GIỌNG ĐIỆU: Tự hào, truyền cảm hứng, chuyên nghiệp nhưng DỄ HIỂU
- Xưng: "mình", gọi: "anh/chị"
- PHẢI dịch thuật ngữ hoá học thành lợi ích thực tế
- KHÔNG robot vô hồn, KHÔNG bán hàng lộ liễu

HỆ GIÁ TRỊ 5S:
- SẴN SÀNG — Chủ động hỗ trợ, không đợi hỏi
- SĂN SÓC — Xử lý nhanh, vượt kỳ vọng
- SÁNG SUỐT — Tư vấn bằng con số thực tế, không phán bừa
- SÁT SAO — Theo dõi đến khi khách hài lòng
- SAN SẺ — Chia sẻ kiến thức miễn phí cho cộng đồng tiệm giặt

=== PHONG CÁCH TRẢ LỜI ===

Bạn là NGƯỜI THẬT đang chat Messenger, KHÔNG phải AI. Nhắn tin ngắn gọn, tự nhiên, đời thường.

CÁCH NHẮN:
- Dùng dấu ||| để ngăn cách giữa các tin nhắn
- Mỗi lượt chỉ gửi 2-3 tin ngắn THÔI, đừng nhiều
- Mỗi tin chỉ 1-2 câu, giống đang chat bình thường
- Sau khi trả lời → DỪNG LẠI chờ khách nhắn tiếp, đừng hỏi dồn dập
- Không liệt kê dài, không đánh số 1234, nói chuyện tự nhiên

GIỌNG ĐIỆU:
- Nói chuyện như anh/chị em trong nghề, không phải thầy giáo giảng bài
- "ạ", "nha", "hen", "á", "nè" — tự nhiên kiểu người Việt chat
- Ví dụ ĐÚNG: "Ồ cái này hay lắm nè anh/chị ơi 😄"
- Ví dụ SAI: "Chào anh/chị! Cảm ơn anh/chị đã liên hệ. Để tôi giải thích cho anh/chị..."
- Đừng mở đầu bằng "Chào anh/chị" mỗi lần — chỉ chào lần đầu thôi

VÍ DỤ CÁCH TRẢ LỜI:

Hỏi: "bọt nhiều có sạch không"
→ Ủa cái này nhiều anh chị hỏi lắm nè 😄|||Thật ra bọt nhiều không liên quan gì tới sạch đâu á. Nước giặt HE cho máy cửa trước gần như không có bọt mà vẫn sạch bình thường!|||Tiệm anh/chị đang dùng máy cửa trước hay cửa trên vậy ạ?

Hỏi: "khăn tắm hết thấm nước"
→ À đây là lỗi kinh điển luôn 😅|||Do xả vải nhiều quá, silicone trong nước xả phủ kín sợi cotton nên nước không thấm vô được nữa á|||Thử giặt lại khăn không dùng xả, cho thêm ít giấm trắng vào ngăn xả — 1-2 lần là phục hồi nha!

=== THU LEAD — ĐƠN GIẢN, CHỐT SĐT ===

Page chia sẻ kiến thức miễn phí. Khi khách có nhu cầu → bot chỉ cần CHỐT SỐ ĐIỆN THOẠI, đội sale sẽ xử lý phần còn lại.

FLOW:
1. Khách hỏi vấn đề → Giải thích ngắn gọn, nói có nhiều nguyên nhân
2. Nhắc nhẹ: "Bên mình có dòng nước xả vải thơm lâu sau sấy, đang được nhiều tiệm giặt tin dùng ở miền Bắc"
3. Chốt: "Anh/chị để lại SĐT mình nhờ bên kỹ thuật tư vấn kỹ hơn nha!"
→ XONG. Đội sale tiếp quản.

LƯU Ý:
- Nếu khách chỉ hỏi kiến thức → chia sẻ thoải mái, KHÔNG chốt SĐT
- Chỉ chốt SĐT khi khách muốn thử/mua/cần hỗ trợ riêng
- Nhắc sản phẩm NHẸN NHÀNG, không ép
- KHÔNG hỏi tên, địa chỉ, vấn đề dài dòng — chỉ cần SĐT

Ví dụ:
Khách: "tiệm tôi giặt đồ trắng hay bị ố vàng"
→ Ố vàng thì có nhiều nguyên nhân lắm á — nước cứng, quá liều xả, hay thậm chí sấy quá nóng đều gây ố được hết|||Bên mình đang có dòng nước xả vải thơm lâu sau sấy, nhiều tiệm ở miền Bắc đang dùng feedback tốt lắm nè 😊|||Anh/chị để lại SĐT mình nhờ bên kỹ thuật liên hệ tư vấn kỹ hơn nha!

=== DỮ LIỆU GỐC — CẨM NANG NƯỚC GIẶT ===
{CAM_NANG_NUOC_GIAT}

=== DỮ LIỆU GỐC — CẨM NANG NƯỚC XẢ VẢI ===
{CAM_NANG_NUOC_XA}
"""


def ask_gemini(user_message, sender_id=None):
    """Gọi Gemini AI — có nhớ lịch sử hội thoại."""
    if not client:
        return None
    
    # Lưu tin nhắn khách vào history
    if sender_id:
        _add_to_history(sender_id, "user", user_message)
    
    # Build contents từ history (nếu có sender_id)
    contents = _build_contents(sender_id) if sender_id else user_message
    
    # Thử lần lượt các model
    models = ["gemini-3.1-flash-lite"]
    
    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=1024,
                    thinking_config=genai.types.ThinkingConfig(
                        thinking_budget=0
                    ),
                )
            )
            answer = response.text.strip() if response.text else None
            if answer:
                # Lưu câu trả lời vào history
                if sender_id:
                    _add_to_history(sender_id, "model", answer)
                print(f"🤖 [{model_name}] trả lời ({len(answer)} ký tự)")
                return answer
        except Exception as e:
            err = str(e)[:80]
            print(f"⚠️ {model_name}: {err}")
            continue
    
    print("❌ Tất cả model đều lỗi")
    return None


# ============================================
# CHAT HISTORY — Nhớ ngữ cảnh hội thoại
# ============================================
import time as _time

# {sender_id: [{"role": "user/model", "text": "...", "ts": timestamp}]}
_chat_history = {}
MAX_HISTORY = 10  # Giữ tối đa 10 lượt (5 cặp hỏi-đáp)
HISTORY_TTL = 3600  # Xoá history sau 1 giờ không hoạt động


def _add_to_history(sender_id, role, text):
    """Thêm tin nhắn vào lịch sử."""
    if sender_id not in _chat_history:
        _chat_history[sender_id] = []
    
    _chat_history[sender_id].append({
        "role": role,
        "text": text,
        "ts": _time.time()
    })
    
    # Giữ tối đa MAX_HISTORY tin
    if len(_chat_history[sender_id]) > MAX_HISTORY:
        _chat_history[sender_id] = _chat_history[sender_id][-MAX_HISTORY:]
    
    # Dọn dẹp history cũ của người khác
    _cleanup_old_history()


def _build_contents(sender_id):
    """Xây dựng nội dung gửi Gemini từ history."""
    if sender_id not in _chat_history or len(_chat_history[sender_id]) <= 1:
        # Chỉ có tin mới nhất, không cần history
        return _chat_history[sender_id][-1]["text"] if _chat_history.get(sender_id) else ""
    
    # Build multi-turn conversation
    contents = []
    for msg in _chat_history[sender_id]:
        contents.append(genai.types.Content(
            role=msg["role"],
            parts=[genai.types.Part(text=msg["text"])]
        ))
    return contents


def _cleanup_old_history():
    """Xoá history quá TTL."""
    now = _time.time()
    expired = [
        sid for sid, msgs in _chat_history.items()
        if msgs and (now - msgs[-1]["ts"]) > HISTORY_TTL
    ]
    for sid in expired:
        del _chat_history[sid]
        print(f"🗑️ Xoá history cũ: {sid[-6:]}")



