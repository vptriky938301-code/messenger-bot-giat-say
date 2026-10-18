# 🌐 HƯỚNG DẪN TRIỂN KHAI BOT LÊN RENDER (24/7 ONLINE)
## Page: Giải Pháp Quà Tặng Doanh Nghiệp

---

## 💡 CƠ CHẾ HOẠT ĐỘNG TRUNG GIAN VỚI GEMINI AI

```
[ Khách hàng nhắn tin trên Messenger ]
                │
                ▼ (Facebook Webhook POST Event)
[ Render Web Service: https://bot-qua-tang-xxxx.onrender.com/webhook ]
                │
                ├── 1. Phản hồi HTTP 200 OK ngay lập tức (< 1s) cho Facebook
                ├── 2. Nhận diện số điện thoại -> Tự động lưu Lead B2B
                │
                ▼ (Gọi Google Gemini API)
[ Google Gemini AI (gemini-2.5-flash) ]
                │  Tư vấn chuyên sâu theo Brand DNA Quà Tặng B2B (ngân sách 50k - 300k, VAT, in logo...)
                │
                ▼ (Facebook Send Message API)
[ Gửi tin nhắn tự động trả lời lại cho Khách hàng trên Messenger ]
```

---

## 📋 THÔNG TIN CẤU HÌNH CẦN ĐIỀN TRÊN RENDER

Khi tạo Web Service trên [Dashboard Render](https://dashboard.render.com), bạn nhập các thông số:

* **Name:** `bot-qua-tang-doanh-nghiep` (hoặc tên tùy thích)
* **Runtime:** `Python`
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn auto_reply_bot:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
* **Plan:** `Free`

### 🔑 Các biến môi trường (Environment Variables) cần thêm trên Render:

| Key | Value | Ghi chú |
|---|---|---|
| `PAGE_ACCESS_TOKEN` | `<Lấy trong file .env cục bộ>` | Token vĩnh viễn của Page Quà Tặng |
| `VERIFY_TOKEN` | `bhs_quatang_verify_2026` | Token xác thực Webhook |
| `GEMINI_API_KEY` | `<Lấy key mới từ Google AI Studio>` | Key kết nối Google Gemini AI (TUYỆT ĐỐI KHÔNG COMMIT LÊN GITHUB) |
| `PYTHON_VERSION` | `3.13.0` | Phiên bản Python chuẩn |

---

## 🚀 3 BƯỚC ĐẨY CODE LÊN GITHUB VÀ CONNECT VỚI RENDER

### Bước 1: Khởi tạo Git & Commit mã nguồn
Mở Terminal trên máy và chạy:
```bash
cd "/Users/pc/Downloads/Học Marketing/Quản Lý Quảng Cáo cho Page Quà Tặng Doanh Nghiệp/M2_Messenger_Bot"
git init
git add .
git commit -m "feat: messenger bot qua tang doanh nghiep with gemini ai"
```

### Bước 2: Tạo Repo mới trên GitHub & Push code
1. Vào [GitHub](https://github.com/new) tạo 1 repo mới (đặt tên ví dụ: `messenger-bot-qua-tang-b2b`, chọn **Private**).
2. Chạy lệnh liên kết và đẩy code lên:
```bash
git remote add origin https://github.com/TÊN_GITHUB_CỦA_BẠN/messenger-bot-qua-tang-b2b.git
git branch -M main
git push -u origin main
```

### Bước 3: Tạo Web Service trên Render
1. Vào [Render Dashboard](https://dashboard.render.com/) > Bấm **New +** > Chọn **Web Service**.
2. Chọn repo GitHub `messenger-bot-qua-tang-b2b` vừa tạo.
3. Điền Build Command, Start Command và các **Environment Variables** như bảng phía trên.
4. Bấm **Deploy Web Service**.
5. Chờ 1-2 phút, Render sẽ cấp cho bạn một đường dẫn URL cố định dạng:
   👉 `https://bot-qua-tang-doanh-nghiep.onrender.com`

---

## 🔗 BƯỚC CUỐI: CÀI ĐẶT WEBHOOK TRÊN FACEBOOK
1. Vào [Meta for Developers](https://developers.facebook.com/) > App của bạn (**App ID: 1325472862695629**).
2. Chọn **Messenger** > **Cài đặt** (Settings) > **Webhooks**.
3. Bấm **Chỉnh sửa URL gọi lại**:
   - **URL gọi lại (Callback URL):** `https://bot-qua-tang-doanh-nghiep.onrender.com/webhook`
   - **Mã xác minh (Verify Token):** `bhs_quatang_verify_2026`
4. Bấm **Xác minh và lưu**.
5. Trong mục **Đăng ký trường của Trang**, chọn Trang **"Giải Pháp Quà Tặng Doanh Nghiệp"** và bật:
   - ✅ `messages`
   - ✅ `messaging_postbacks`

🎉 **Hoàn tất!** Từ lúc này, bot sẽ chạy tự động 24/7 trên Cloud Render, không cần treo máy tính của bạn nữa!
