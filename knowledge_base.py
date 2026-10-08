"""
📚 KNOWLEDGE BASE — Giải Pháp Quà Tặng Doanh Nghiệp (Bách Hóa Sạch 2S)
Cơ sở dữ liệu kiến thức sản phẩm, gói quà tặng B2B, chính sách chiết khấu, VAT, hợp đồng.
"""

# ============================================
# 1. THÔNG TIN DOANH NGHIỆP & ĐỊNH VỊ
# ============================================
BRAND_INFO = {
    "brand_name": "Giải Pháp Quà Tặng Doanh Nghiệp — Bách Hóa Sạch 2S",
    "factory": "Nhà máy sản xuất đạt chuẩn ISO, hơn 20 năm kinh nghiệm trong ngành hóa mỹ phẩm tiêu dùng.",
    "hotline": "098x.xxx.xxx",
    "email": "quatang.bachhoasach2s@gmail.com",
    "positioning": (
        "Cung cấp giải pháp quà tặng tiêu dùng thiết thực (Nước giặt, Nước lau sàn, Nước rửa chén, Nước rửa tay) "
        "dành cho Doanh nghiệp, Công đoàn xí nghiệp, Nhà máy khu công nghiệp, Trường học và Tổ chức. "
        "Cam kết: 100% người nhận đều sử dụng được hàng ngày — Không lãng phí — Tối ưu chi phí ngân sách."
    ),
    "core_benefits": [
        "100% hàng thiết yếu gia đình, ai cũng dùng được ngay",
        "Chiết khấu tận xưởng sản xuất, tối ưu ngân sách từ 50.000đ đến 300.000đ+",
        "Hỗ trợ in ấn Logo thương hiệu, thiệp chúc mừng, đóng hộp quà Tết sang trọng",
        "Đầy đủ hóa đơn đỏ VAT hợp lệ, hợp đồng kinh tế minh bạch cho kế toán",
        "Giao hàng tận nơi toàn quốc, hỗ trợ chia theo từng chi nhánh/nhà máy",
        "Gửi bộ mẫu thử (Sample Box) tận văn phòng cho ban trù bị duyệt trước"
    ]
}

# ============================================
# 2. CÁC GÓI QUÀ TẶNG THEO NGÂN SÁCH
# ============================================
GIFT_PACKAGES = {
    "duoi_100k": {
        "name": "Set Tiết Kiệm — Quà Tặng Công Nhân / Số Lượng Lớn",
        "budget": "50.000đ – 85.000đ / suất",
        "target": "Phù hợp nhà máy xí nghiệp đông công nhân (từ 200 đến hàng chục nghìn suất), ngân sách vừa phải.",
        "combo_options": [
            {
                "combo_id": "TK01",
                "items": ["Nước rửa chén Caro Lô Hội 750g", "Nước lau sàn Caro Bưởi 980g"],
                "packing": "Túi quà quai xách đỏ Tết / Túi kraft trang nhã kèm thiệp",
                "price_estimate": "Khoảng 55.000đ – 65.000đ (tùy số lượng)"
            },
            {
                "combo_id": "TK02",
                "items": ["Nước rửa tay Carose 500ml", "Nước lau sàn Caro 980g"],
                "packing": "Túi quà in logo doanh nghiệp",
                "price_estimate": "Khoảng 65.000đ – 75.000đ"
            }
        ]
    },
    "100k_150k": {
        "name": "Set Phổ Thông — Gắn Kết & Ấm Áp (Bán Chạy Nhất)",
        "budget": "100.000đ – 150.000đ / suất",
        "target": "Phù hợp quà Tết công đoàn, quà sinh nhật nhân viên, quà tri ân khách hàng thân thiết.",
        "combo_options": [
            {
                "combo_id": "PT01",
                "items": ["Can Nước giặt cao cấp Lozzi 2.4kg (Hương nước hoa Pháp)", "Nước rửa chén Caro 750g"],
                "packing": "Hộp quà Tết có quai xách sang trọng / Hộp carton in offset",
                "price_estimate": "Khoảng 105.000đ – 120.000đ (tùy số lượng)"
            },
            {
                "combo_id": "PT02",
                "items": ["Can Nước giặt Lozzi 2.4kg", "Nước lau sàn Caro Bưởi 980g", "Thiệp chúc mừng thiết kế riêng"],
                "packing": "Hộp quà nắp gài cao cấp",
                "price_estimate": "Khoảng 125.000đ – 145.000đ"
            }
        ]
    },
    "180k_250k": {
        "name": "Set Tri Ân — Thịnh Vượng & Chu Đáo",
        "budget": "180.000đ – 250.000đ / suất",
        "target": "Dành cho cán bộ quản lý, nhân viên xuất sắc, khách hàng VIP hoặc đối tác kinh doanh.",
        "combo_options": [
            {
                "combo_id": "TA01",
                "items": [
                    "Can Nước giặt cao cấp Lozzi 3.6kg (Hương nước hoa)",
                    "Nước lau sàn Caro Bưởi 980g",
                    "Nước rửa chén Caro Lô Hội 750g"
                ],
                "packing": "Hộp quà cứng cao cấp phủ nhũ, in logo nổi mạ kim",
                "price_estimate": "Khoảng 190.000đ – 220.000đ"
            }
        ]
    },
    "300k_plus": {
        "name": "Set VIP — Toàn Diện & Đẳng Cấp",
        "budget": "300.000đ – 450.000đ+ / suất",
        "target": "Quà tặng lãnh đạo, đối tác chiến lược, hội nghị khách hàng quy mô lớn.",
        "combo_options": [
            {
                "combo_id": "VIP01",
                "items": [
                    "Can Nước giặt cao cấp Lozzi can lớn",
                    "Bộ đôi Lau sàn Caro + Rửa chén Caro",
                    "Nước rửa tay Carose 500ml",
                    "Bộ tẩy cặn canxi Movex A cao cấp"
                ],
                "packing": "Vali quà tặng / Giỏ quà phong cách sang trọng độc bản",
                "price_estimate": "Khoảng 320.000đ – 420.000đ"
            }
        ]
    }
}

# ============================================
# 3. DANH MỤC SẢN PHẨM CHI TIẾT
# ============================================
PRODUCTS = {
    "lozzi": {
        "name": "Nước giặt cao cấp Lozzi",
        "variants": ["Can 2.4kg", "Can 3.6kg", "Can 4.0kg"],
        "scents": ["Hương Nước Hoa Pháp Quyến Rũ", "Hương Cá Ngựa Sang Trọng"],
        "highlights": "Công nghệ enzyme bóc tách vết bẩn cứng đầu, giữ bền màu vải, lưu hương thơm ngát suốt 7 ngày, an toàn lành tính cho da tay."
    },
    "caro_lau_san": {
        "name": "Nước lau sàn Caro",
        "variants": ["Chai 980g", "Can 3.8kg"],
        "scents": ["Hương Tinh Dầu Bưởi Hồng", "Hương Quế Tự Nhiên"],
        "highlights": "Khử khuẩn nhanh, đuổi côn trùng, sàn khô nhanh không nhờn dính, hương thơm thư thái dễ chịu."
    },
    "caro_rua_chen": {
        "name": "Nước rửa chén Caro",
        "variants": ["Chai 750g", "Can 3.8kg"],
        "scents": ["Chiết xuất Lô Hội & Chanh Tươi"],
        "highlights": "Sạch bóng dầu mỡ thức ăn, khử sạch mùi tanh hải sản, tinh chất lô hội mềm dịu không khô rát da tay."
    },
    "carose_rua_tay": {
        "name": "Nước rửa tay kháng khuẩn Carose 500ml",
        "variants": ["Chai vòi nhấn 500ml"],
        "highlights": "Diệt khuẩn 99.9%, bổ sung vitamin E dưỡng ẩm tay, mùi hương thanh mát nhẹ nhàng."
    },
    "movex": {
        "name": "Bộ tẩy rửa chuyên dụng Movex",
        "variants": ["Tẩy cặn canxi Movex A 500ml", "Siêu tẩy dầu mỡ đa năng Movex"],
        "highlights": "Đánh bay cặn canxi vách kính phòng tắm, thiết bị vệ sinh sáng bóng chỉ sau 3 phút."
    }
}

# ============================================
# 4. CHÍNH SÁCH B2B & FAQ DOANH NGHIỆP
# ============================================
B2B_POLICIES = {
    "vat": "Bách Hóa Sạch 2S xuất đầy đủ hóa đơn GTGT (VAT) điện tử hợp pháp cho mọi đơn hàng doanh nghiệp.",
    "contract": "Có đầy đủ Hợp đồng kinh tế, biên bản giao nhận, phiếu kiểm định chất lượng xuất xưởng (CO/CQ).",
    "branding": "Miễn phí thiết kế và dán Decal/in Logo doanh nghiệp lên set quà cho đơn từ 100 suất trở lên.",
    "sample": "Hỗ trợ gửi mẫu thử nguyên set (Sample Kit) miễn phí tận văn phòng cho ban trù bị/công đoàn đánh giá trực tiếp.",
    "delivery": "Giao hàng đúng hẹn tận kho, phân bổ nhiều điểm hoặc nhà xưởng theo yêu cầu.",
    "lead_time": "Thời gian sản xuất & đóng gói: 3 – 7 ngày làm việc tùy số lượng."
}

# ============================================
# 5. HÀM TRA CỨU KIẾN THỨC THEO TỪ KHÓA
# ============================================
def find_quatang_topic(user_text: str):
    """Phân loại ý định người dùng để trả lời nhanh chính xác."""
    text = user_text.lower().strip()
    
    # Hỏi về ngân sách / giá cả
    if any(k in text for k in ["giá", "ngân sách", "bao nhiêu", "chi phí", "báo giá", "bảng giá"]):
        return "bao_gia"
    
    # Hỏi về quà Tết
    if any(k in text for k in ["tết", "quà tết", "năm mới", "cuối năm"]):
        return "qua_tet"
    
    # Hỏi về công đoàn / công nhân
    if any(k in text for k in ["công đoàn", "công nhân", "nhân viên", "phúc lợi", "nhà máy", "xí nghiệp"]):
        return "cong_doan"
    
    # Hỏi về hóa đơn VAT, hợp đồng
    if any(k in text for k in ["vat", "hóa đơn", "hợp đồng", "thuế", "chứng từ"]):
        return "vat_hop_dong"
    
    # Hỏi về in logo, bao bì
    if any(k in text for k in ["in logo", "thương hiệu", "bao bì", "hộp", "túi", "thiết kế"]):
        return "in_logo"
    
    # Hỏi về mẫu thử
    if any(k in text for k in ["mẫu", "xem mẫu", "sample", "dùng thử"]):
        return "mau_thu"
    
    # Xin catalog
    if any(k in text for k in ["catalog", "catalogue", "tài liệu", "file"]):
        return "catalog"
        
    return None
