"""
📚 KHO KIẾN THỨC — Bí Quyết Giặt Sấy Dân Sinh
Trích xuất từ: Cẩm nang Nước Giặt, Cẩm nang Nước Xả, 
13 bài kiến thức TikTok, Lead Magnets, Bài viết T9/2026

Dùng cho bot Messenger tự động trả lời câu hỏi chủ tiệm giặt.

=== BRAND DNA BHS 2S (TUÂN THỦ BẮT BUỘC) ===
- Page: Bí Quyết Giặt Sấy Dân Sinh (page lạnh, kênh chia sẻ kiến thức)
- Chuyên ngành: Hoá chất giặt là chuyên dụng
- Khách hàng mục tiêu: Chủ tiệm giặt là dân sinh
- Thương hiệu gốc: Bách Hoá Sạch 2S (BHS 2S)
- Sản phẩm: LOZZI (nước giặt), CARO (nước lau sàn), MoveX (tẩy rửa), DEFA (đa năng)

HÌNH MẪU THƯƠNG HIỆU:
  Chuyên gia — kiến thức chuyên sâu, nói bằng bằng chứng khoa học
  + Người Chăm sóc — đồng cảm, nhẹ nhàng, chia sẻ

TÍNH CÁCH: Đam mê, Chân thành, Tử tế
GIỌNG ĐIỆU: Tự hào, truyền cảm hứng, chuyên nghiệp nhưng dễ hiểu
  → Dịch thuật ngữ hoá học thành lợi ích thực tế
  → Xưng "mình", gọi "anh/chị/bạn"
  → KHÔNG robot vô hồn, KHÔNG bán hàng lộ liễu

HỆ GIÁ TRỊ CỐT LÕI 5S:
  SẴN SÀNG — Chủ động hỗ trợ, không đợi hỏi
  SĂN SÓC — Xử lý nhanh, vượt kỳ vọng khách hàng
  SÁNG SUỐT — Tư vấn bằng con số thực tế, không phán bừa
  SÁT SAO — Theo dõi đến khi khách hài lòng
  SAN SẺ — Chia sẻ kiến thức miễn phí cho cộng đồng tiệm giặt

LỜI HỨA: Sản phẩm đúng chất lượng, dịch vụ tận tâm
"""

# ============================================
# KEYWORD → TOPIC MAPPING
# ============================================
KEYWORD_MAP = {
    # Máy giặt & vận hành
    "máy giặt": "may_giat",
    "cửa ngang": "may_giat",
    "cửa đứng": "may_giat",
    "lồng giặt": "may_giat",
    "vệ sinh lồng": "may_giat",
    "tải trọng": "may_giat",
    "vắt": "may_giat",
    "sấy": "may_giat",
    "máy sấy": "may_giat",
    "bảo dưỡng": "may_giat",

    # Hóa chất & nước giặt
    "nước giặt": "nuoc_giat",
    "bột giặt": "nuoc_giat",
    "hóa chất": "nuoc_giat",
    "hoạt chất": "nuoc_giat",
    "surfactant": "nuoc_giat",
    "đậm đặc": "nuoc_giat",
    "pha muối": "nuoc_giat",
    "lozzi": "nuoc_giat",
    "defa": "nuoc_giat",
    "bhs": "nuoc_giat",

    # Nước xả & hương thơm
    "nước xả": "nuoc_xa",
    "xả vải": "nuoc_xa",
    "hương thơm": "nuoc_xa",
    "mùi thơm": "nuoc_xa",
    "esterquats": "nuoc_xa",
    "silicone": "nuoc_xa",
    "làm mềm": "nuoc_xa",
    "caro": "nuoc_xa",
    "movex": "nuoc_xa",

    # Tẩy vết bẩn
    "vết bẩn": "tay_vet",
    "tẩy": "tay_vet",
    "mốc": "tay_vet",
    "ố vàng": "tay_vet",
    "dầu mỡ": "tay_vet",
    "vết dầu": "tay_vet",
    "javel": "tay_vet",
    "oxy": "tay_vet",
    "son": "tay_vet",
    "máu": "tay_vet",

    # Bọt & định lượng
    "bọt": "dinh_luong",
    "định lượng": "dinh_luong",
    "ml": "dinh_luong",
    "bao nhiêu": "dinh_luong",
    "tiết kiệm": "dinh_luong",
    "chi phí": "dinh_luong",
    "tốn": "dinh_luong",
    "lãng phí": "dinh_luong",

    # Vận hành tiệm giặt
    "tiệm giặt": "van_hanh",
    "mở tiệm": "van_hanh",
    "kinh doanh": "van_hanh",
    "nhân viên": "van_hanh",
    "giá dịch vụ": "van_hanh",
    "khách hàng": "van_hanh",
    "vốn": "van_hanh",
    "lợi nhuận": "van_hanh",
    "sop": "van_hanh",
    "quy trình": "van_hanh",

    # Mùi hôi & xử lý
    "hôi": "mui_hoi",
    "mùi hôi": "mui_hoi",
    "chua": "mui_hoi",
    "khai": "mui_hoi",
    "ẩm mốc": "mui_hoi",
    "mùa mưa": "mui_hoi",
}

# ============================================
# KHO KIẾN THỨC THEO CHỦ ĐỀ
# ============================================
KNOWLEDGE = {
    "may_giat": {
        "title": "🔧 Kỹ thuật máy giặt & vận hành",
        "answer": (
            "📌 6 lỗi phổ biến khi dùng máy giặt cửa ngang:\n\n"
            "1️⃣ Đóng kín cửa sau giặt → bí hơi, gây mốc nấm & hôi lồng\n"
            "✅ Mở hé 5-10cm là chuẩn nhất\n\n"
            "2️⃣ Không khóa vòi nước → ống cấp luôn ở áp suất âm, dễ bùng vòi ngập nhà\n\n"
            "3️⃣ Đổ sai ngăn hóa chất:\n"
            "• Ngăn trái: Nước giặt chính\n"
            "• Ngăn giữa: Nước xả vải\n"
            "• Ngăn phải: Nước tẩy\n"
            "⚠️ Trộn tẩy + xả chung → trung hòa hóa chất, mất mùi thơm!\n\n"
            "4️⃣ Nhồi quá 70% lồng → giặt không sạch, hại motor\n"
            "✅ Tốt nhất: 50-60% dung tích\n\n"
            "5️⃣ Không vệ sinh cửa xả cặn khẩn cấp (góc dưới máy)\n\n"
            "6️⃣ Dùng nước giặt nhiều bọt cho cửa ngang → trào qua khe, hỏng bo mạch\n"
            "✅ BẮT BUỘC dùng nước giặt ít bọt (bọt kiểm soát)"
        )
    },
    
    "nuoc_giat": {
        "title": "🧴 Kiến thức nước giặt",
        "answer": (
            "📌 Bột giặt vs Nước giặt cho tiệm:\n\n"
            "🔴 Bột giặt:\n"
            "• Rẻ, tẩy bùn đất tốt\n"
            "• Nhưng: pH >10 (kiềm cao), khó tan, đọng cặn trắng, hại sợi vải\n\n"
            "🟢 Nước giặt:\n"
            "• Tan 100%, bảo vệ sợi vải, giữ màu\n"
            "• Phù hợp máy cửa ngang\n\n"
            "⚠️ CẢNH BÁO nước giặt pha muối:\n"
            "Cơ sở gia công rẻ chỉ cho 3-5% hoạt chất, rồi đổ muối NaCl làm đặc quánh.\n"
            "Hậu quả: Muối ăn mòn lồng inox, tạo cặn vôi, gây ố vàng áo trắng!\n\n"
            "✅ Nước giặt đậm đặc chuẩn: 15-17% hoạt chất, chỉ cần 40-50ml/mẻ 10kg\n"
            "💰 Chi phí: chỉ 550-750đ/kg đồ"
        )
    },
    
    "nuoc_xa": {
        "title": "🌸 Kiến thức nước xả vải",
        "answer": (
            "📌 Nước xả vải — Thành phần & cách dùng:\n\n"
            "🔬 3 loại chất làm mềm:\n"
            "• Quats (thế hệ cũ): Mềm nhưng không phân hủy sinh học\n"
            "• Esterquats (thế hệ mới): Mềm + phân hủy được + giữ hương lâu\n"
            "• Silicone: Mềm mượt nhất nhưng tạo lớp phủ, giảm thấm hút\n\n"
            "⚠️ Sai lầm phổ biến:\n"
            "• Đổ nhiều xả = thơm lâu? SAI! Quá nhiều tạo lớp sáp bít sợi vải\n"
            "• Trộn xả + tẩy chung 1 ngăn → trung hòa, mất công dụng cả hai\n\n"
            "✅ Công thức tiệm giặt chuẩn:\n"
            "Nước giặt đa năng KHÔNG mùi (sạch sâu) + Nước xả chuyên dụng hương lâu\n"
            "→ Hoặc: Giặt sạch + xịt thơm sau sấy (giữ hương 7-10 ngày)"
        )
    },
    
    "tay_vet": {
        "title": "🧹 Mẹo tẩy vết bẩn chuyên sâu",
        "answer": (
            "📌 Xử lý vết bẩn theo từng loại:\n\n"
            "🔴 Vết dầu mỡ khô:\n"
            "• Xịt chất nhũ hóa/tẩy mỡ TRƯỚC khi bỏ vào máy\n"
            "• Tuyệt đối KHÔNG vò xà phòng khô → loang màu!\n\n"
            "🟡 Vết mốc chăn ga:\n"
            "• Ngâm ấm 40°C với Enzyme/tẩy mốc oxy hóa\n"
            "• KHÔNG dùng Javel nồng độ cao → mục sợi bông!\n\n"
            "🟢 Vết bùn đất mùa mưa:\n"
            "• Để khô → chải/phủi bùn khô trước\n"
            "• KHÔNG xả nước trực tiếp lên bùn ướt → ngấm sâu vào thớ vải!\n\n"
            "🔵 Oxy vs Javel:\n"
            "• Javel (Natri Hypochlorite): Tẩy trắng mạnh nhưng ăn mòn sợi vải, phai màu\n"
            "• Oxy (Sodium Percarbonate): Nhẹ hơn, an toàn với màu, dùng được đồ màu"
        )
    },
    
    "dinh_luong": {
        "title": "📊 Định lượng & tiết kiệm chi phí",
        "answer": (
            "📌 Bảng định lượng nước giặt đậm đặc (15-17% hoạt chất):\n\n"
            "🔹 Máy 9kg: 35-40ml/mẻ\n"
            "🔹 Máy 12kg: 45-55ml/mẻ\n"
            "🔹 Máy 16kg: 60-70ml/mẻ\n"
            "🔹 Máy 20kg: 80-90ml/mẻ\n\n"
            "⚠️ Bài toán thất thoát:\n"
            "• 20 mẻ/ngày x thừa 20ml = lãng phí 400ml/ngày\n"
            "• 1 tháng: mất 12 lít nước giặt\n"
            "• 1 năm: ném qua cửa sổ gần 150 lít → ~18 TRIỆU ĐỒNG!\n\n"
            "💡 Mẹo kiểm soát:\n"
            "• Dùng ca đong có vạch ml, không múc áng chừng\n"
            "• In bảng định lượng dán tường cạnh máy giặt\n"
            "• Giặt nhanh 15-20p chỉ dùng 1/4 lượng bình thường"
        )
    },
    
    "van_hanh": {
        "title": "🏪 Vận hành tiệm giặt",
        "answer": (
            "📌 Checklist vận hành tiệm giặt:\n\n"
            "🔹 SOP hàng ngày:\n"
            "• Kiểm tra túi quần áo khách trước khi giặt\n"
            "• Phân loại: trắng/màu, nặng/nhẹ, dính bẩn/bình thường\n"
            "• Ghi sổ mẻ giặt: số kg, loại đồ, hóa chất dùng\n"
            "• Vệ sinh lồng giặt cuối ngày\n\n"
            "🔹 Chi phí vận hành tham khảo:\n"
            "• Nước giặt đậm đặc: 550-750đ/kg đồ\n"
            "• Nước xả: 200-350đ/kg đồ\n"
            "• Điện + nước: ~1.000-1.500đ/kg đồ\n"
            "• Tổng giá vốn: ~2.000-2.500đ/kg\n\n"
            "💰 Giá dịch vụ phổ biến:\n"
            "• Giặt sấy thường: 15.000-25.000đ/kg\n"
            "• Giặt hấp/dry clean: 30.000-80.000đ/kg\n"
            "→ Biên lợi nhuận: 40-60% nếu kiểm soát hóa chất tốt"
        )
    },
    
    "mui_hoi": {
        "title": "👃 Xử lý mùi hôi & ẩm mốc",
        "answer": (
            "📌 Nguyên nhân & cách xử lý mùi hôi:\n\n"
            "🔴 Mùi hôi chua sau sấy:\n"
            "• Nguyên nhân: Vi khuẩn phát triển khi đồ ướt để lâu trước sấy\n"
            "• Hoặc: Nước giặt xả không sạch bọt, cặn lên men\n"
            "✅ Giải pháp: Giặt xong sấy ngay trong 30 phút, không để qua đêm\n\n"
            "🟡 Mùi hôi lồng giặt:\n"
            "• Nguyên nhân: Nấm mốc mặt sau lồng inox + cặn xà phòng\n"
            "✅ Vệ sinh lồng hàng tháng bằng chất tẩy lồng chuyên dụng\n"
            "✅ Bảo dưỡng cơ khí 8-12 tháng/lần\n\n"
            "🟢 Mùa mưa đồ không khô:\n"
            "• Vắt ở tốc độ cao nhất trước khi sấy\n"
            "• Phân loại dày/mỏng trước khi sấy\n"
            "• Vệ sinh bộ lọc sấy → giảm 30% thời gian sấy"
        )
    }
}

# ============================================
# TIN NHẮN DÍ DỎM KHI KHÔNG HIỂU
# (Giọng: Chuyên gia + Người Chăm sóc, chân thành, không robot)
# ============================================
import random

FUN_REPLIES = [
    (
        "Haha anh/chị vui tính ghê! 😄\n\n"
        "Mình chuyên về hoá chất giặt là thôi nha — "
        "nhưng lĩnh vực này thì mình tự tin tư vấn chuẩn luôn! 💪\n\n"
        "Thử hỏi mình đi, ví dụ:\n"
        "• \"Máy giặt cửa ngang dùng sao cho đúng?\"\n"
        "• \"Tẩy vết mốc chăn ga kiểu gì?\"\n"
        "• \"Bao nhiêu ml nước giặt cho máy 12kg?\"\n\n"
        "Hoặc gõ 1/2/3 để nhận cẩm nang miễn phí! 📚"
    ),
    (
        "Ơ câu này thì mình chịu rồi ạ 😅\n\n"
        "Mình là dân R&D hoá chất — chuyên giúp anh chị chủ tiệm giặt "
        "tiết kiệm chi phí và giặt sạch hơn thôi! 🧺\n\n"
        "Anh/chị thử hỏi về:\n"
        "🔬 Hoá chất giặt tẩy (nước giặt, nước xả...)\n"
        "🔧 Mẹo vận hành máy giặt\n"
        "📊 Bảng định lượng ml tiết kiệm\n"
        "👃 Xử lý mùi hôi đồ giặt\n\n"
        "Mình sẵn sàng hỗ trợ ạ! 🙌"
    ),
    (
        "Ui câu hỏi này vượt ngoài chuyên môn mình rồi 🤣\n\n"
        "Nhưng mà về giặt là thì mình trả lời vanh vách luôn!\n"
        "Ví dụ:\n"
        "• \"Giặt áo trắng sao không bị ố vàng?\"\n"
        "• \"Nước giặt pha muối nguy hiểm thế nào?\"\n"
        "• \"Chi phí vận hành tiệm giặt bao nhiêu?\"\n\n"
        "Hỏi thử đi anh/chị — mình giải thích dễ hiểu, "
        "không dùng từ hàn lâm đâu! 😎"
    ),
    (
        "Anh/chị ơi, mình là trợ lý kiến thức giặt là, "
        "không phải Siri đâu nha 😆\n\n"
        "Nhưng mà cái gì liên quan đến giặt giũ thì cứ hỏi:\n"
        "• Tại sao đồ giặt xong vẫn hôi chua?\n"
        "• Bột giặt hay nước giặt tốt hơn cho tiệm?\n"
        "• Máy giặt 12kg dùng bao nhiêu ml nước giặt?\n\n"
        "Gõ 1 để nhận Cẩm nang Nước Giặt 📘\n"
        "Gõ 2 để nhận Cẩm nang Nước Xả 📗\n"
        "Gõ 3 để nhận cả 2 bộ! 📚"
    ),
]

def get_fun_reply():
    """Trả lời dí dỏm ngẫu nhiên khi không hiểu tin nhắn."""
    return random.choice(FUN_REPLIES)

MSG_KHONG_HIEU = FUN_REPLIES[0]  # Fallback mặc định

def find_topic(message_text):
    """Tìm topic phù hợp nhất dựa trên keywords trong tin nhắn."""
    text = message_text.lower()
    topic_scores = {}
    
    for keyword, topic in KEYWORD_MAP.items():
        if keyword in text:
            topic_scores[topic] = topic_scores.get(topic, 0) + 1
    
    if topic_scores:
        # Trả về topic có nhiều keyword match nhất
        best_topic = max(topic_scores, key=topic_scores.get)
        return best_topic
    
    return None

def get_answer(topic):
    """Lấy câu trả lời theo topic."""
    if topic and topic in KNOWLEDGE:
        info = KNOWLEDGE[topic]
        return f"{info['title']}\n\n{info['answer']}"
    return None
