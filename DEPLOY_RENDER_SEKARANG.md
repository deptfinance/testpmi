# 🚀 DEPLOY KE RENDER - STEP BY STEP (IKUTI EXACT!)

**Waktu: ~5 menit**

---

## 🎯 DATA YANG ANDA BUTUHKAN:

```
GitHub Repository: https://github.com/deptfinance/testpmi
Branch: claude/pmi-data-scraper-gga9xo
Telegram Token: 8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw
```

---

## 🚀 STEP 1: BUKA RENDER.COM

1. **Buka browser** → https://render.com
2. **Login/Sign up** (bisa pake GitHub)
3. **Authorize** Render untuk akses GitHub Anda

---

## ➕ STEP 2: BUAT WEB SERVICE

Setelah login di Render dashboard:

1. **Klik "New +"** (tombol di atas/kanan)
2. **Pilih "Web Service"**

```
┌─────────────────────────────────────┐
│  New +                              │
├─────────────────────────────────────┤
│  □ Blueprint                        │
│  □ Web Service          ← PILIH INI │
│  □ Static Site                      │
│  □ Private Service                  │
└─────────────────────────────────────┘
```

---

## 🔗 STEP 3: CONNECT REPOSITORY

Halaman **"Create a Web Service"**:

1. **Connect a repository:**
   - Cari: `testpmi`
   - Klik repo: `deptfinance/testpmi`
   - Klik **"Connect"**

Kalau tidak ketemu:
- Click **"Configure GitHub App"**
- Allow akses ke repository `testpmi`
- Coba search lagi

---

## ⚙️ STEP 4: CONFIGURE SERVICE

Halaman setup service - isi sesuai:

### **Bagian 1: Basic Info**

```
Name:           cek-pmi-bot
Branch:         claude/pmi-data-scraper-gga9xo
Root Directory: (kosongkan)
Runtime:        Docker
Region:         Singapore (atau pilihan lain)
Plan:           Free
```

### **Bagian 2: Build & Deploy**

```
Dockerfile:      Dockerfile.render
Build Command:   (kosongkan - Docker auto)
Start Command:   python3 main.py
```

### **Bagian 3: Environment Variables**

Klik **"Add Environment Variable"**:

```
Key:   TELEGRAM_TOKEN
Value: 8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw
```

Klik **"Add"**

---

## 🚀 STEP 5: CREATE & DEPLOY

1. **Scroll ke bawah**
2. **Klik "Create Web Service"**
3. **Tunggu deployment** (3-5 menit)

Render akan:
- ✅ Clone repo dari GitHub
- ✅ Build Docker image
- ✅ Install dependencies
- ✅ Start bot service
- ✅ Assign URL

---

## ⏳ MONITORING DEPLOYMENT

Saat deployment, Anda akan lihat:

**Status bar:**
```
Building image... → Pushing image... → Deploying... → Live ✓
```

**Logs:**
Akan tampil real-time logs dari container:
```
Step 1/X : FROM mcr.microsoft.com/playwright:v1.40.0-jammy
Step 2/X : WORKDIR /app
...
Running: python3 main.py
✓ Bot siap menerima pesan dari Telegram...
```

Kalau ada error, akan tampil di logs merah.

---

## ✅ VERIFIKASI BOT RUNNING

### **Check 1: Lihat Status di Dashboard**

```
Dashboard → cek-pmi-bot service
Status harus: 🟢 Running (hijau)
```

### **Check 2: Lihat Logs**

```
Dashboard → cek-pmi-bot → Logs
Scroll down, harus ada:
"✓ Bot siap menerima pesan dari Telegram..."
```

### **Check 3: Test di Telegram**

1. **Buka Telegram**
2. **Cari bot** pakai token (atau buka chat dengan bot)
3. **Kirimkan: `/start`**
   - Bot harus balik: "👋 Selamat datang di Bot Cek PMI!"

4. **Kirimkan: `/cek AU610053`**
   - Bot akan tampilkan: "⏳ Mengecek data PMI..."
   - Proses 5-10 detik
   - Bot balik dengan data atau error message

---

## 🎉 JIKA BERHASIL:

Bot Anda sudah **ONLINE 24/7** di Render! 🚀

Siapapun bisa pakai dengan membuka Telegram dan kirimkan nomor paspor.

---

## ❌ JIKA ADA ERROR:

### **Error 1: Build Failed**

**Check logs untuk error detail:**
- Missing file?
- Syntax error?
- Dependency issue?

**Fix:**
1. Fix error di code
2. Push ke GitHub
3. Render auto-redeploy

### **Error 2: Service Crashed**

**Check logs:**
- Token invalid?
- Network error?
- Playwright issue?

**Fix:**
1. Check token valid di @BotFather
2. Manual Deploy (button di dashboard)
3. Lihat logs untuk error detail

### **Error 3: Bot tidak respond di Telegram**

**Kemungkinan:**
- Deployment belum selesai (tunggu 3-5 min)
- Token salah
- Bot crashed

**Debug:**
1. Check status: 🟢 Running?
2. Check logs: Ada error?
3. Restart: Click "Manual Deploy"

---

## 📊 RENDER DASHBOARD OVERVIEW:

```
Dashboard (Home)
  └─ cek-pmi-bot (Service)
     ├─ Overview (status, URL, config)
     ├─ Logs (real-time logs)
     ├─ Events (deployment history)
     ├─ Settings (edit config, env vars)
     └─ Metrics (CPU, memory, requests)
```

---

## 🔄 SETELAH DEPLOY SELESAI:

### **Auto-Redeploy on GitHub Push:**

```bash
# Edit code lokal
nano main.py

# Commit & push
git add .
git commit -m "Update bot"
git push origin claude/pmi-data-scraper-gga9xo

# Render akan auto-redeploy dalam 1-2 menit
# Check di Render dashboard → Events
```

### **Manual Restart:**

Jika perlu restart bot tanpa push:
1. Buka Render dashboard
2. Klik service "cek-pmi-bot"
3. Klik **"Manual Deploy"** button
4. Bot akan restart dalam 30 detik

### **Change Environment Variable:**

1. Buka service
2. Klik **"Settings"**
3. Edit **"TELEGRAM_TOKEN"**
4. Klik **"Save"**
5. Bot otomatis restart

---

## 📞 QUICK CHECKLIST:

### **Pre-Deployment:**
- [ ] GitHub repo ready
- [ ] Code pushed ke branch: `claude/pmi-data-scraper-gga9xo`
- [ ] Telegram token siap: `8829845272:AAFIr...`
- [ ] Render account created

### **During Deployment:**
- [ ] Repository connected di Render
- [ ] Service name: `cek-pmi-bot`
- [ ] Runtime: Docker
- [ ] Dockerfile: `Dockerfile.render`
- [ ] Start Command: `python3 main.py`
- [ ] TELEGRAM_TOKEN set
- [ ] Plan: Free (atau Starter)
- [ ] Click "Create Web Service"

### **Post-Deployment:**
- [ ] Wait 3-5 menit
- [ ] Check logs: "Bot siap..."
- [ ] Status: 🟢 Running
- [ ] Test di Telegram: `/start`
- [ ] Test Cek PMI: `/cek AU610053`
- [ ] Bot respond correctly
- [ ] ✅ DONE!

---

## 🎯 SELESAI!

Bot Anda sudah **LIVE 24/7** di Render! 🎉

Siapapun bisa akses bot via Telegram dan check data PMI!

---

## 📚 DOKUMENTASI TAMBAHAN:

- **RENDER_DEPLOY.md** - Detail lengkap
- **RENDER_QUICK.txt** - Quick reference
- **TROUBLESHOOTING.md** - Troubleshooting guide

---

**Siap mulai? Buka https://render.com dan ikuti STEP 1-5!** 🚀
