# 🤖 Panduan Setup Telegram Bot Cek PMI

## 📋 Prerequisites

- Python 3.7+
- pip (package manager)
- Telegram account & app
- Server atau komputer untuk menjalankan bot (24/7)

---

## 🚀 Step-by-Step Setup

### **STEP 1: Install Dependencies**

```bash
# Linux/Mac
pip3 install -r requirements.txt
python3 -m playwright install chromium

# Windows
pip install -r requirements.txt
python -m playwright install chromium
```

### **STEP 2: Jalankan Bot**

```bash
# Linux/Mac
python3 bot_pmi.py

# Windows
python bot_pmi.py
```

**Expected Output:**
```
============================================================
🤖 BOT CECK PMI - TELEGRAM
============================================================

✓ Bot sedang dijalankan...
✓ Token: 8829845272:AAFIr5...

Bot menunggu pesan dari user...

Press Ctrl+C to stop the bot
```

### **STEP 3: Gunakan Bot di Telegram**

1. **Cari bot** di Telegram: `@YourBotUsername` (ganti dengan username bot Anda)
   
2. **Kirim pesan** ke bot dengan nomor paspor:
   ```
   AU610053
   ```

3. **Bot akan**:
   - Membaca nomor paspor Anda
   - Otomatis mengecek ke BP2MI
   - Mengirimkan hasil dalam format rapi

4. **Hasil yang didapat**:
   ```
   ✅ DATA PMI DITEMUKAN

   👤 Nama
   Budi Santoso

   🌍 Negara Penempatan
   Arab Saudi

   🏢 P3MI (Pemberi Kerja)
   PT Karya Bersama

   🤝 Mitra LN
   Al Rajhi

   📍 Alamat
   Jl. Merdeka No. 42, Jakarta

   📅 Berlaku Hingga
   2025-12-31
   
   ✅ Data berhasil diambil dari BP2MI
   ```

---

## 📱 Fitur Bot

### **Commands:**

| Command | Fungsi |
|---------|--------|
| `/start` | Tampilkan pesan sambutan |
| `/help` | Tampilkan panduan penggunaan |
| `/info` | Info tentang bot |

### **Message Handling:**

- User kirim nomor paspor (contoh: AU610053)
- Bot otomatis process dan return hasil
- Validasi format otomatis
- Error handling yang jelas

---

## 🔧 Konfigurasi

### **Mengganti Token Bot**

Jika ingin menggunakan bot Telegram lain, edit `bot_pmi.py`:

```python
TELEGRAM_BOT_TOKEN = "YOUR_NEW_TOKEN_HERE"
```

Caranya:
1. Buka BotFather di Telegram: `@BotFather`
2. Pilih `/newbot` dan ikuti instruksi
3. Copy token dan paste di `bot_pmi.py`

---

## 📊 Cara Kerja Bot

```
User ─────────────────────────────────────► Telegram Bot
                                              │
                                              ├─ Validasi input
                                              │
                                              ├─ Jalankan cek_pmi.py
                                              │
                                              ├─ Buka website BP2MI
                                              │
                                              ├─ Pecahkan captcha
                                              │
                                              ├─ Extract data
                                              │
User ◄──────────────────────────────────────  └─ Format & kirim hasil
```

---

## 🌐 Deployment (Menjalankan 24/7)

Untuk bot berjalan 24 jam, ada beberapa opsi:

### **Option 1: Komputer Lokal (Simple)**
- Jalankan `python3 bot_pmi.py`
- Komputer harus selalu menyala
- Cocok untuk testing/dev

### **Option 2: Server Cloud (Recommended)**

**Heroku (Gratis tier discontinued, tapi bisa pakai alternatif)**
- Render.com
- Railway.app
- PythonAnywhere
- DigitalOcean

**Contoh dengan Railway.app:**

1. Push code ke GitHub
2. Connect repository ke Railway
3. Set environment variable: `TELEGRAM_BOT_TOKEN`
4. Deploy otomatis

### **Option 3: VPS/Cloud VM (Paling Reliable)**

- AWS EC2
- Google Cloud VM
- Azure VM
- DigitalOcean Droplet

**Setup di VPS:**
```bash
# 1. SSH ke server
ssh user@your-server.com

# 2. Clone repository
git clone <repo-url>
cd testpmi

# 3. Install dependencies
pip3 install -r requirements.txt
python3 -m playwright install chromium

# 4. Jalankan dengan systemd (opsional, untuk auto-restart)
sudo nano /etc/systemd/system/bot-pmi.service
```

**Systemd Service File:**
```ini
[Unit]
Description=PMI Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/testpmi
ExecStart=/usr/bin/python3 /home/ubuntu/testpmi/bot_pmi.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable bot-pmi
sudo systemctl start bot-pmi
sudo systemctl status bot-pmi
```

---

## 🐛 Troubleshooting

### **Error 1: "Invalid token"**
**Solusi:** Token sudah expired atau salah
- Cek token di BotFather
- Pastikan tidak ada spasi atau karakter aneh

### **Error 2: "Connection refused"**
**Solusi:** Tidak ada internet atau VPN issue
- Check koneksi internet
- Coba connect ke proxy jika di kantor

### **Error 3: "Website not accessible"**
**Solusi:** BP2MI website down atau blocked
- Tunggu beberapa saat
- Cek status website di browser

### **Error 4: "Bot stopped working"**
**Solusi:** Proses crash atau timeout
- Check logs untuk error message
- Restart bot dengan `python3 bot_pmi.py`
- Jika di server, check dengan `systemctl status bot-pmi`

### **Error 5: Bot tidak merespon**
**Solusi:** Polling tidak aktif
- Pastikan bot script masih running
- Check apakah token masih valid
- Lihat logs untuk error

---

## 📊 Monitoring Bot

### **Check Bot Status:**

```bash
# Linux/Mac
ps aux | grep bot_pmi.py

# Windows
tasklist | find "python"
```

### **View Bot Logs:**

Tambahkan logging ke file:
```python
# Di bot_pmi.py tambahkan:
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

Lihat logs:
```bash
tail -f bot.log
```

---

## 📈 Future Improvements

Fitur yang bisa ditambahkan:

- [ ] Database untuk cache hasil
- [ ] Statistics/analytics
- [ ] Multiple language support
- [ ] Schedule tasks (cek otomatis)
- [ ] Export ke Excel/PDF
- [ ] Admin dashboard
- [ ] Rate limiting
- [ ] User authentication

---

## 📞 Support

Jika ada issue:
1. Check troubleshooting section
2. Lihat logs untuk error message
3. Verifikasi token & network
4. Coba restart bot
5. Hubungi developer jika masih error

---

## 📝 License & Credits

**Bot Cek PMI v1.0**
- Powered by Python + Playwright + Telegram Bot API
- Data source: BP2MI (Badan Pelindung Pekerja Migran Indonesia)

Gunakan dengan bijak! 🙏

---

**Happy botting! 🚀**
