# 🚀 RENDER.COM DEPLOYMENT GUIDE

Bot akan deploy ke Render.com dengan Docker. Render gratis untuk 1 service pertama!

---

## 📋 REQUIREMENTS:

- GitHub account (dengan repo ini)
- Render.com account (gratis di https://render.com)
- Telegram Bot Token (dari @BotFather)

---

## 🚀 STEP-BY-STEP DEPLOYMENT:

### **STEP 1: Push ke GitHub**

```bash
# Masuk ke folder project
cd /path/to/cek-pmi-bot

# Inisialisasi git
git init
git add .
git commit -m "Initial commit - PMI checker bot for Render"

# Tambah remote GitHub
git remote add origin https://github.com/USERNAME/cek-pmi-bot.git

# Push ke GitHub
git branch -M main
git push -u origin main
```

**Ganti `USERNAME` dengan GitHub username Anda.**

---

### **STEP 2: Setup Render Account**

1. **Buka** https://render.com
2. **Sign up** gratis (bisa pake GitHub)
3. **Authorize** dengan GitHub

---

### **STEP 3: Create Web Service di Render**

1. **Di Render dashboard**, klik **"New +"**
2. **Pilih** "Web Service"
3. **Connect GitHub repo**:
   - Search: `cek-pmi-bot`
   - Select repository
   - Click "Connect"

---

### **STEP 4: Configure Service**

**Di halaman setup:**

#### **Basic Settings:**
- **Name:** `cek-pmi-bot`
- **Runtime:** `Docker`
- **Region:** `Singapore` (atau terdekat)
- **Plan:** `Free` (unlimited free tier)

#### **Build & Deploy:**
- **Dockerfile:** `Dockerfile.render`
- **Build Command:** (biarkan kosong, Docker auto-build)
- **Start Command:** `python3 main.py`

#### **Environment Variables:**
Klik "Add Environment Variable":
```
Key: TELEGRAM_TOKEN
Value: [Paste token dari @BotFather]
```

---

### **STEP 5: Deploy**

1. **Click "Create Web Service"**
2. Render akan:
   - ✅ Clone repo dari GitHub
   - ✅ Build Docker image
   - ✅ Install dependencies
   - ✅ Start bot service

3. **Tunggu deployment** (3-5 menit)

**Lihat logs real-time di Render dashboard.**

---

## ✅ VERIFIKASI DEPLOYMENT:

### **Check 1: Lihat Logs di Render**

1. Buka Render dashboard
2. Klik service "cek-pmi-bot"
3. Lihat "Logs" tab
4. Harus ada: `Bot siap menerima pesan dari Telegram...`

### **Check 2: Test di Telegram**

1. **Buka Telegram**
2. **Cari bot** pakai token Anda
3. **Kirimkan** `/start`
4. Bot harus balik: "👋 Selamat datang di Bot Cek PMI!"

### **Check 3: Test Cek PMI**

1. **Kirimkan** `/cek AU610053`
2. Bot harus:
   - Tampilkan "⏳ Mengecek data PMI..."
   - Proses 5-10 detik
   - Balik dengan data PMI atau error message

---

## 📊 RENDER DASHBOARD:

**Main Tabs:**

```
Logs          ← Real-time bot logs
Events        ← Deployment history
Settings      ← Config & env vars
Metrics       ← CPU, memory, requests
```

---

## 🔧 MANAGE SERVICE:

### **Restart Bot:**
1. Buka service
2. Click "Manual Deploy"
3. Click "Deploy latest commit"
4. Bot akan restart dalam 30 detik

### **Change Environment Variable:**
1. Go to "Settings"
2. Edit "TELEGRAM_TOKEN"
3. Click "Save"
4. Bot otomatis restart

### **Check Status:**
- Green dot = Running
- Yellow dot = Building/Deploying
- Red dot = Error

### **View Logs:**
```
Logs → Real-time logs dari bot
       Search dengan keywords
       Download sebagai file
```

---

## 💰 PRICING (Render.com):

**Free Tier:**
- ✅ 1 free web service
- ✅ 750 compute hours/month
- ✅ Auto-sleep setelah 15 menit idle (cold start ~30-60 detik)
- ✅ Cukup untuk 1 bot

**Starter Plan ($7/month):**
- No auto-sleep
- 24/7 running
- Better performance

**Recommended:** Pakai free tier dulu, upgrade ke Starter jika diperlukan.

---

## ⚠️ COLD START ISSUE:

**Free tier:**
- Bot idle → sleep after 15 minutes
- First request akan lambat (30-60 detik)
- Request berikutnya normal speed

**Solution:**
- Upgrade ke Starter ($7/month)
- Atau biarkan, user akan tunggu

---

## 🐛 TROUBLESHOOTING:

### **ERROR 1: "Build failed"**

**Check logs untuk error detail.**

Common causes:
- Missing dependencies → Check requirements.txt
- Wrong Dockerfile path → Verify Dockerfile.render
- Token format error → Check TELEGRAM_TOKEN format

**Fix:**
1. Check logs
2. Fix error di code
3. Push to GitHub
4. Render auto-redeploy

### **ERROR 2: "Service crashed"**

**Check logs → Lihat error message.**

**Common causes:**
- Token invalid
- Network error
- Playwright issue

**Fix:**
1. Check token valid di @BotFather
2. Restart service (Manual Deploy)
3. Check logs untuk error

### **ERROR 3: Bot tidak respond**

**Kemungkinan:**

| Gejala | Cause | Fix |
|--------|-------|-----|
| Bot tidak ada di Telegram | Service belum running | Wait 2-3 minutes |
| Bot ada tapi tidak respond | Token invalid | Check token |
| Bot respond error | Network issue | Check logs |
| Slow response | Cold start | Wait first request |

---

## 📝 AUTO-REDEPLOY ON PUSH:

Render otomatis redeploy saat Anda push ke GitHub!

```bash
# Buat change di code
echo "# Update" >> README.md

# Push ke GitHub
git add .
git commit -m "Update bot"
git push

# Render akan auto-redeploy dalam 1-2 menit
# Check di Render dashboard → Deployments
```

---

## 🔐 SECURITY:

### **Keep Token Secret:**

```bash
# JANGAN push token ke GitHub!
# Gunakan environment variable di Render
# (sudah setup di render.yaml)
```

### **Check in Code:**
- main.py sudah pakai `os.environ.get()`
- Token tidak hardcoded di code
- Safe untuk push ke GitHub

---

## 📞 NEXT STEPS:

1. **Push ke GitHub** dengan struktur folder sudah siap
2. **Buat Render account** di render.com
3. **Connect repo** ke Render
4. **Set TELEGRAM_TOKEN** environment variable
5. **Deploy** - Done!

---

## ✨ FEATURES:

✅ **Free hosting** - Gratis dengan Render  
✅ **Auto-redeploy** - Push → Auto-redeploy  
✅ **Logs streaming** - Real-time logs  
✅ **One-click restart** - Easy management  
✅ **Custom domain** - Available (paid)  
✅ **Discord alerts** - Integration available  

---

## 🎯 DEPLOYMENT CHECKLIST:

- [ ] GitHub account ready
- [ ] Push code ke GitHub
- [ ] Render account created
- [ ] Service connected ke GitHub repo
- [ ] TELEGRAM_TOKEN set di env vars
- [ ] Dockerfile.render selected
- [ ] Deployment started
- [ ] Check logs - Bot running?
- [ ] Test di Telegram - Works?
- [ ] ✅ Done! Bot 24/7 online!

---

## 📚 DOKUMENTASI LENGKAP:

- **Render Docs:** https://render.com/docs
- **Docker Docs:** https://docs.docker.com
- **Telegram Bot API:** https://core.telegram.org/bots

---

**Ready? Push ke GitHub dan deploy ke Render sekarang!** 🚀🤖
