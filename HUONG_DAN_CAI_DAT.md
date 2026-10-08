# 🤖 HƯỚNG DẪN CÀI ĐẶT & CHẠY CHATBOT QUÀ TẶNG DOANH NGHIỆP
## Page: Giải Pháp Quà Tặng Doanh Nghiệp (Page ID: `1301661599686717`)

---

## 📌 1. Trạng Thái Cấu Hình Hiện Tại
- **Page Access Token:** Đã được tích hợp sẵn trong file `.env` (Token vĩnh viễn cấp riêng cho Page).
- **Verify Token:** `bhs_quatang_verify_2026`
- **Bộ não AI:** Google Gemini AI (hỗ trợ tư vấn theo ngân sách 50k - 300k+, set quà Tết, quà công đoàn, hóa đơn VAT, in logo).
- **Hệ thống chốt Lead:** Tự động bắt số điện thoại và lưu vào `data/leads_quatang.json`.
- **Cổng chạy mặc định:** `http://localhost:5001`

---

## 🚀 2. Các Bước Khởi Chạy Bot

### Bước 1: Khởi động Server Bot
Mở Terminal trên máy Mac và chạy lệnh:
```bash
cd "/Users/pc/Downloads/Học Marketing/Quản Lý Quảng Cáo cho Page Quà Tặng Doanh Nghiệp/M2_Messenger_Bot"
python3 auto_reply_bot.py
```
Khi thấy dòng thông báo sau là server đã sẵn sàng:
```
✅ Gemini AI đã kết nối thành công (key: ...kyf0Zs)
🚀 Bot Quà Tặng Doanh Nghiệp đang chạy tại cổng http://localhost:5001
🔗 Webhook Verify Token: bhs_quatang_verify_2026
```

---

### Bước 2: Tạo đường dẫn công khai (Tunnel ra Internet)
Mở một cửa sổ Terminal mới và chạy một trong hai công cụ:

**Cách 1: Dùng Cloudflared (Miễn phí, không cần đăng nhập)**
```bash
cloudflared tunnel --url http://localhost:5001
```
*(Copy đường dẫn https dạng: `https://xxxx-xxxx.trycloudflare.com`)*

**Cách 2: Dùng Ngrok**
```bash
ngrok http 5001
```
*(Copy đường dẫn https dạng: `https://xxxx.ngrok-free.app`)*

---

### Bước 3: Điền Webhook trên Meta Developers
1. Truy cập [Meta for Developers](https://developers.facebook.com/apps/) → Chọn App của bạn (**App ID: 1325472862695629**).
2. Vào mục **Messenger** > **Cài đặt** (Settings) > **Webhooks**.
3. Bấm **Chỉnh sửa URL gọi lại** (Edit Callback URL):
   - **URL gọi lại (Callback URL):** `https://đường-dẫn-tunnel-của-bạn/webhook`
   - **Mã xác minh (Verify Token):** `bhs_quatang_verify_2026`
4. Bấm **Xác minh và lưu** (Verify and Save).
5. Trong mục **Đăng ký trường của Trang** (Page Subscriptions), chọn Page **"Giải Pháp Quà Tặng Doanh Nghiệp"** và tích chọn:
   - ✅ `messages`
   - ✅ `messaging_postbacks`

---

## 🎯 3. Kiểm Tra & Theo Dõi Lead
- **Nhắn tin thử:** Dùng tài khoản Facebook cá nhân nhắn tin vào Page "Giải Pháp Quà Tặng Doanh Nghiệp" các câu như:
  - *"Bên mình có quà Tết cho công nhân không?"*
  - *"Ngân sách tầm 100k - 120k có set nào?"*
  - *"SĐT mình là 0912345678, gửi báo giá qua Zalo cho mình nhé"*
- **Xem danh sách Lead:** Mở file:
  `Quản Lý Quảng Cáo cho Page Quà Tặng Doanh Nghiệp/M2_Messenger_Bot/data/leads_quatang.json`
