# 🤖 HƯỚNG DẪN CÀI ĐẶT MESSENGER BOT
## Page: Bí Quyết Giặt Sấy Dân Sinh

---

## ✅ Đã hoàn thành

- [x] Clone repo `pragnakalp/facebook-messenger-bot-python`
- [x] Tạo virtual environment Python
- [x] Cài Flask + requests

## ⚠️ Cần làm trước khi chạy

### Bước 1: Tạo Facebook App (nếu chưa có)
1. Vào [Meta for Developers](https://developers.facebook.com/)
2. Tạo App mới → Chọn **Business** type
3. Thêm product **Messenger**

### Bước 2: Lấy Page Access Token
1. Trong App > Messenger > Settings
2. Chọn Page **"Bí Quyết Giặt Sấy Dân Sinh"**
3. Generate Token → Copy

### Bước 3: Cấu hình biến môi trường
```bash
cp .env.example .env
# Sửa file .env: điền PAGE_ACCESS_TOKEN và VERIFY_TOKEN
```

### Bước 4: Chạy bot local
```bash
cd facebook-messenger-bot
source venv/bin/activate
python facebook_bot.py
```
Bot sẽ chạy trên `http://localhost:5000`

### Bước 5: Expose ra internet (cho Facebook Webhook)
Cần tool tunneling để Facebook gọi được webhook:
```bash
# Cách 1: ngrok (miễn phí)
ngrok http 5000

# Cách 2: cloudflared (miễn phí)
cloudflared tunnel --url http://localhost:5000
```

### Bước 6: Setup Webhook trên Facebook
1. Vào App > Messenger > Settings > Webhooks
2. Callback URL: `https://your-ngrok-url.ngrok.io`
3. Verify Token: nhập giống trong `.env`
4. Subscribe: `messages`, `messaging_postbacks`

---

## 📁 Cấu trúc thư mục

```
facebook-messenger-bot/
├── facebook_bot.py      # Source code chính
├── requirements.txt     # Dependencies
├── .env.example         # Mẫu cấu hình
├── .env                 # Cấu hình thật (tự tạo)
├── venv/                # Virtual environment
├── HUONG_DAN_CAI_DAT.md # File này
└── README.md            # Hướng dẫn gốc từ repo
```

## 🔗 Liên kết với kế hoạch Ads

Bot này phục vụ **Phần 3 của kế hoạch**: tự động gửi link cẩm nang Giặt Xả khi lead nhắn tin qua Messenger từ bài CTA Cold/Remarketing.

Tham chiếu:
- [Kế hoạch triển khai app](../06_KE_HOACH_DU_TINH_TRIEN_KHAI_APP_ADS.md)
- [Kế hoạch ads phễu T10](../../01_Bach_Hoa_Sach_2S/Bao_Cao_Chien_Dich/Ke_Hoach_Ads_Xay_Pheu_T10_2026.md)
