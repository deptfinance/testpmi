# 🚀 START HERE - DEPLOY BOT ANDA SEKARANG!

Saya sudah siapkan semua untuk Anda. Tinggal pilih 1 method dan jalankan!

---

## ⚡ PALING MUDAH (Railway.app - Gratis!)

**Tidak perlu install apa-apa di komputer Anda**

1. **Buka** → https://railway.app
2. **Sign up** dengan GitHub
3. **Click** → "New Project" 
4. **Choose** → "Deploy from GitHub repo"
5. **Select** → Repository: `deptfinance/testpmi`
6. **Branch** → `claude/pmi-data-scraper-gga9xo`
7. **Click** → "Deploy"
8. **Tunggu** → 2-3 menit bot akan running

**Selesai! Bot sudah siap 24/7** ✅

**Cara pakai bot:**
- Buka Telegram
- Kirimkan nomor paspor: `AU610053`
- Bot akan balik dengan data!

---

## 💻 JIKA PAKAI DOCKER (Lokal)

**Docker sudah installed?** → Mari jalankan 1 command:

```bash
git clone https://github.com/deptfinance/testpmi.git
cd testpmi
git checkout claude/pmi-data-scraper-gga9xo
docker-compose up -d
```

**Done!** Bot running 24/7 di background.

Buka Telegram dan gunakan bot!

---

## 🖥️ JIKA PAKAI KOMPUTER (Linux/Mac)

```bash
# Download
git clone https://github.com/deptfinance/testpmi.git
cd testpmi
git checkout claude/pmi-data-scraper-gga9xo

# Install (hanya sekali)
bash install_linux_mac.sh

# Jalankan bot
python3 bot_pmi.py
```

Selesai! Bot running. Buka Telegram dan gunakan.

**Untuk auto-start (optional):**
```bash
sudo cp bot-pmi.service /etc/systemd/system/
sudo systemctl enable bot-pmi.service
sudo systemctl start bot-pmi.service
```

Bot akan otomatis start setiap kali komputer boot.

---

## 🪟 JIKA PAKAI WINDOWS

1. **Download** repository
2. **Buka file** → `install_windows.bat`
3. **Double-click** → Install semua dependencies
4. **Buka file** → `run_bot.bat`
5. **Double-click** → Bot mulai running!

Buka Telegram dan gunakan bot!

**Untuk auto-start (optional):**
1. Buat file `run_bot.bat`:
   ```batch
   @echo off
   cd /d %~dp0
   python bot_pmi.py
   ```

2. Buka **Task Scheduler** (Win+R → `taskschd.msc`)
3. Create Basic Task:
   - Name: "PMI Bot"
   - Trigger: "At startup"
   - Action: Run program → `run_bot.bat`
4. Done! Bot auto-start setiap boot.

---

## 📱 CARA PAKAI BOT DI TELEGRAM:

**Setelah bot running:**

1. **Buka Telegram**
2. **Kirimkan** `/start`
   - Bot akan balik dengan pesan sambutan
3. **Kirimkan nomor paspor** (contoh: `AU610053`)
   - Bot akan cek ke BP2MI
   - Bot akan balik dengan data lengkap
4. **Selesai!** 🎉

---

## 🎯 QUICK COMPARISON:

| Method | Setup | 24/7? | Kemudahan |
|--------|-------|-------|-----------|
| **Railway** ⭐ | 5 menit | ✅ | ⭐⭐⭐⭐⭐ Paling mudah |
| Docker Compose | 10 menit | ✅ | ⭐⭐⭐⭐ Mudah |
| Linux/Mac | 10 menit | ✅ | ⭐⭐⭐ Medium |
| Windows | 15 menit | ✅ | ⭐⭐⭐ Medium |

**Rekomendasi:** Railway.app untuk kemudahan maksimal!

---

## ✅ CEK BOT RUNNING:

```bash
# Linux/Mac (Systemd)
sudo systemctl status bot-pmi.service

# Docker
docker ps | grep pmi

# Railway
Buka dashboard Railway → lihat logs
```

---

## ❌ TROUBLESHOOTING:

**Bot tidak respond:**
- Check apakah bot running
- Coba restart bot
- Pastikan token valid

**Bot crash terus:**
- Check logs untuk error message
- Install dependencies ulang
- Restart bot

**Network error:**
- Check internet connection
- Coba lagi dalam beberapa saat

---

## 📖 DOKUMENTASI LENGKAP:

Baca file `DEPLOY_NOW.md` untuk info detail tentang setiap method.

---

## 🎉 DONE!

Pilih 1 method di atas dan deploy sekarang!

**Bot sudah ready untuk 24/7 operation.**

Enjoy! 🚀

---

## 📞 KONTAK:

- **Repository:** https://github.com/deptfinance/testpmi
- **Branch:** `claude/pmi-data-scraper-gga9xo`
- **Token:** `8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw`

---

**Ready? Pilih method dan mulai deploy! 🚀**
