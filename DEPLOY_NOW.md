# 🚀 DEPLOYMENT GUIDE - READY TO USE NOW!

Bot Telegram Anda sudah siap untuk di-deploy! Pilih salah satu method di bawah:

---

## 🎯 PILIH CARA DEPLOYMENT:

### **Option 1: RAILWAY.APP (Paling Mudah - Gratis!)**

Bot akan langsung running 24/7 di cloud Railway.

**Step-by-Step:**

1. **Buka:** https://railway.app
2. **Sign up** dengan GitHub account
3. **Click:** "New Project" → "Deploy from GitHub repo"
4. **Select:** Repository `deptfinance/testpmi`
5. **Choose:** Branch `claude/pmi-data-scraper-gga9xo`
6. **Environment Variables:** Tidak perlu diubah (token sudah ada di code)
7. **Deploy** - Done! 

Bot akan mulai running dalam 1-2 menit. Selesai!

**Cek status:**
- Buka Railway dashboard
- Lihat logs untuk confirm bot running

**Akses bot:**
- Buka Telegram
- Cari bot (berdasarkan token)
- Kirimkan nomor paspor
- Bot akan balas dengan data PMI

---

### **Option 2: DOCKER (Lokal / VPS)**

Untuk menjalankan di komputer lokal atau server Anda dengan Docker.

**Requirements:**
- Docker installed (https://www.docker.com/products/docker-desktop)

**Step-by-Step:**

```bash
# 1. Clone repo
git clone https://github.com/deptfinance/testpmi.git
cd testpmi
git checkout claude/pmi-data-scraper-gga9xo

# 2. Build image
docker build -t pmi-bot .

# 3. Run container
docker run -d --name pmi-bot --restart always pmi-bot

# 4. Check logs
docker logs pmi-bot

# 5. Stop (jika perlu)
docker stop pmi-bot
docker rm pmi-bot
```

Bot akan running terus (restart otomatis jika crash).

**Akses bot:**
- Buka Telegram
- Gunakan bot seperti normal

---

### **Option 3: DOCKER COMPOSE (Lokal - Recommended)**

Paling mudah untuk setup lokal dengan Docker.

**Requirements:**
- Docker & Docker Compose installed

**Step-by-Step:**

```bash
# 1. Clone repo
git clone https://github.com/deptfinance/testpmi.git
cd testpmi
git checkout claude/pmi-data-scraper-gga9xo

# 2. Start bot
docker-compose up -d

# 3. View logs
docker-compose logs -f pmi-bot

# 4. Stop (jika perlu)
docker-compose down
```

Bot akan running 24/7. Bahkan setelah reboot, bot akan otomatis start.

---

### **Option 4: SYSTEMD SERVICE (Linux/Mac - Simple)**

Untuk Linux/Mac tanpa Docker.

**Requirements:**
- Linux/Mac
- Python 3.7+
- Sudo access

**Step-by-Step:**

```bash
# 1. Clone repo
git clone https://github.com/deptfinance/testpmi.git
cd testpmi
git checkout claude/pmi-data-scraper-gga9xo

# 2. Install dependencies
pip3 install -r requirements.txt
python3 -m playwright install chromium

# 3. Setup systemd service
sudo cp bot-pmi.service /etc/systemd/system/
sudo sed -i 's|/home/ubuntu/testpmi|'$(pwd)'|g' /etc/systemd/system/bot-pmi.service
sudo sed -i 's|ubuntu|'$(whoami)'|g' /etc/systemd/system/bot-pmi.service

# 4. Enable & start service
sudo systemctl daemon-reload
sudo systemctl enable bot-pmi.service
sudo systemctl start bot-pmi.service

# 5. Check status
sudo systemctl status bot-pmi.service

# 6. View logs
sudo journalctl -u bot-pmi.service -f
```

Bot akan **otomatis start** setiap kali komputer diboot!

**Manage service:**
```bash
# Stop
sudo systemctl stop bot-pmi.service

# Start
sudo systemctl start bot-pmi.service

# Restart
sudo systemctl restart bot-pmi.service

# View logs
sudo journalctl -u bot-pmi.service -n 100 -f
```

---

### **Option 5: WINDOWS - TASK SCHEDULER**

Untuk menjalankan bot otomatis di Windows.

**Step-by-Step:**

1. **Clone repo & install:**
   ```cmd
   git clone https://github.com/deptfinance/testpmi.git
   cd testpmi
   git checkout claude/pmi-data-scraper-gga9xo
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

2. **Buat .bat file** - `run_bot.bat`:
   ```batch
   @echo off
   cd /d %~dp0
   python bot_pmi.py
   ```

3. **Open Task Scheduler** (Win+R → `taskschd.msc`)

4. **Create Basic Task:**
   - Name: "PMI Bot"
   - Trigger: "At startup"
   - Action: Start program → `run_bot.bat`
   - Check: "Run whether user is logged in or not"

5. **Done!** Bot akan auto-start setiap kali Windows boot.

---

## ⚡ QUICK SUMMARY:

| Method | Setup Time | 24/7? | Cost | Best For |
|--------|-----------|-------|------|----------|
| Railway | 5 menit | ✅ | Free | Cloud, 24/7, easiest |
| Docker Compose | 10 menit | ✅ | Free | Local, simple |
| Systemd | 10 menit | ✅ | Free | Linux, auto-start |
| Task Scheduler | 15 menit | ✅ | Free | Windows, auto-start |
| Docker | 10 menit | ✅ | Free | Production, flexible |

---

## 🎯 RECOMMENDED (Pilihan Terbaik):

**Untuk kemudahan maksimal:**
👉 **Railway.app** - Paling simple, tidak perlu install apa-apa di komputer

**Untuk yang sudah punya Docker:**
👉 **Docker Compose** - 1 command, langsung jalan

**Untuk Linux/Mac tanpa Docker:**
👉 **Systemd Service** - Auto-start otomatis

**Untuk Windows:**
👉 **Task Scheduler** - Built-in Windows

---

## ✅ VERIFIKASI BOT RUNNING:

Setelah deploy, test dengan:

1. **Buka Telegram**
2. **Cari bot** (gunakan token di code: `8829845272:AAFIr5...`)
3. **Kirimkan:** `/start`
4. **Harusnya bot balas** dengan pesan sambutan
5. **Kirimkan nomor paspor:** `AU610053`
6. **Bot akan proses** dan balik dengan data (atau error jika tidak ada)

---

## 🆘 TROUBLESHOOTING:

### Bot tidak respond
- Check apakah bot running (lihat logs)
- Check token valid
- Restart bot

### Logs menunjukkan error
```bash
# Railway: lihat Railway dashboard
# Docker: docker logs pmi-bot
# Systemd: sudo journalctl -u bot-pmi.service -f
```

### Bot crash terus
- Check error message di logs
- Verify token valid
- Pastikan Chromium terinstall

### Port conflicts
- Systemd/Docker: check tidak ada port conflicts
- Change port jika perlu

---

## 📞 NEXT STEPS:

1. **Pilih 1 method** dari 5 di atas
2. **Follow step-by-step** sesuai method
3. **Test di Telegram** dengan `/start`
4. **Enjoy!** Bot sudah ready 24/7 🎉

---

## 💾 GIT INFO:

- **Repository:** https://github.com/deptfinance/testpmi
- **Branch:** `claude/pmi-data-scraper-gga9xo`
- **Token:** `8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw`

---

**Ready? Pilih salah satu method dan deploy! 🚀**
