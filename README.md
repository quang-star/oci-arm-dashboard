# OCI ARM Dashboard 🚀

Giao diện web theo dõi và điều khiển tiến trình săn VPS Oracle Cloud **Always Free Ampere A1 (2 OCPU / 12 GB RAM / 100 GB Disk)** tại Osaka (`ap-osaka-1`).

## Kiến trúc
- **Frontend:** Vue 3 + Vite + Tailwind CSS, deploy 1-click lên **Vercel**.
- **Backend API:** Python FastAPI siêu nhẹ (~25MB RAM) chạy dưới dạng systemd service trên máy chủ VPS.
- **Bảo mật:** Sử dụng Secret API Key và kết nối qua domain HTTPS, không hardcode IP hay thông tin nhạy cảm.

---

## 1. Triển khai Backend lên VPS

Trước khi cài service, tạo `/etc/catcher-api.env` trên VPS với nội dung `DASHBOARD_API_KEY=<key-rieng-ngau-nhien>` và chỉ cho root đọc (`sudo chmod 600 /etc/catcher-api.env`). Không đưa key vào repo.

Chạy lệnh sau trên máy của bạn để đưa backend lên VPS:

```bash
# Copy thư mục backend lên VPS
scp -i <path-to-ssh-key> -r ./backend ubuntu@<your-vps-domain-or-ip>:/home/ubuntu/dashboard-backend

# Chạy script cài đặt service systemd
ssh -i <path-to-ssh-key> ubuntu@<your-vps-domain-or-ip> "bash /home/ubuntu/dashboard-backend/setup-service.sh"
```

Service Backend sẽ tự động chạy ngầm trên port `8000` và khởi động cùng hệ thống.

---

## 2. Triển khai Frontend lên Vercel

1. Đẩy repo lên GitHub:
   ```bash
   git add .
   git commit -m "feat: initial commit"
   git push -u origin main
   ```
2. Trên Vercel Dashboard:
   - **Root Directory:** Chọn thư mục `frontend`
   - **Environment Variables:**
     - `VITE_API_URL`: URL Backend (ví dụ `https://api-arm.quanglab.site`)
     - Không đặt API key trong biến `VITE_`: các giá trị này được công khai trong trình duyệt. Nhập key qua giao diện dashboard.
3. Bấm **Deploy**.

---

## 3. Sử dụng Dashboard
- Mở link dashboard trên trình duyệt.
- Bấm nút chìa khóa 🔑 trên góc phải để tùy chỉnh Backend URL hoặc API Key bất cứ lúc nào.
- Bấm **Bật Săn (Start)** để bắt đầu chu kỳ kiểm tra tự động.
- Theo dõi log thời gian thực trên khung Terminal tích hợp.
