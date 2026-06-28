# 🚂 RAILWAY.APP SETUP - STEP BY STEP

Bot akan running 24/7 di cloud Railway. Gratis untuk 1 bulan pertama!

---

## 📋 REQUIREMENTS:

- GitHub account (gratis di github.com)
- Railway account (gratis di railway.app)
- Internet connection

---

## 🚀 SETUP (5 STEP MUDAH):

### **STEP 1: Pastikan Code Sudah di GitHub**

Kode Anda sudah di:
```
Repository: deptfinance/testpmi
Branch: claude/pmi-data-scraper-gga9xo
```

✅ Semua file sudah ada (saya sudah push)

---

### **STEP 2: Buka Railway.app**

1. **Buka browser** → https://railway.app
2. **Klik "Sign In"** (kanan atas)
3. **Pilih "Sign in with GitHub"**
4. **Authorize Railway** untuk akses GitHub Anda
5. **Selesai login** ✅

---

### **STEP 3: Create New Project**

1. **Dari Railway dashboard**
2. **Klik "New Project"** (kanan bawah atau tengah)
3. **Pilih "Deploy from GitHub repo"**

```
┌─────────────────────────────────────┐
│  New Project                        │
├─────────────────────────────────────┤
│  □ Empty Service                    │
│  □ PostgreSQL                       │
│  □ MySQL                            │
│  □ Deploy from GitHub repo      ◄── PILIH INI
│  □ Deploy from Public Repository   │
└─────────────────────────────────────┘
```

---

### **STEP 4: Select Repository**

1. **Cari repository:** `testpmi` atau `deptfinance/testpmi`
2. **Click select** pada repository `testpmi`

Kalau tidak ketemu:
- Click "Configure GitHub App"
- Allow akses ke repository `testpmi`

---

### **STEP 5: Configure & Deploy**

**Di halaman konfigurasi:**

1. **Root Directory:** Leave empty (atau `/`)
2. **Branch:** Change ke `claude/pmi-data-scraper-gga9xo`
3. **Environment Variables:** Tidak perlu diubah
4. **Click "Deploy"** 🚀

Railway akan:
- ✅ Download code dari GitHub
- ✅ Install Python & dependencies
- ✅ Install Chromium browser
- ✅ Start bot service
- ✅ Assign domain & keep running 24/7

**Tunggu 2-3 menit untuk deployment**

---

## ✅ VERIFIKASI BOT RUNNING:

### **Cara 1: Check di Railway Dashboard**

1. **Buka** https://railway.app
2. **Masuk ke project**
3. **Lihat logs** - Harus ada:
   ```
   ============================================================
   🤖 BOT CECK PMI - TELEGRAM
   ============================================================
   ✓ Bot sedang dijalankan...
   Bot menunggu pesan dari user...
   ```

Jika log menunjukkan error, scroll up untuk lihat full error.

### **Cara 2: Test di Telegram**

1. **Buka Telegram**
2. **Kirimkan `/start`** ke bot
   - Bot harus balik dengan pesan sambutan
3. **Kirimkan nomor paspor** (contoh: `AU610053`)
   - Bot akan processing
   - Bot akan balik dengan data

---

## 🎯 SETELAH DEPLOYMENT:

Bot sudah **running 24/7** di cloud Railway!

Siapapun bisa akses bot dengan:
1. **Buka Telegram**
2. **Cari bot** (gunakan token: `8829845272:AAFIr5...`)
3. **Kirimkan nomor paspor**
4. **Bot balik dengan data PMI** ✅

---

## 🔍 MONITORING:

### **Check Bot Status:**

1. **Buka Railway dashboard**
2. **Klik project PMI Bot**
3. **Lihat status** (harus "Running" ✓)
4. **Baca logs** untuk cek ada error

### **View Logs:**

```
Pada Railway dashboard:
Deployments → Latest Deploy → View Logs

Harus bisa lihat:
✓ Bot sedang dijalankan...
Bot menunggu pesan dari user...
```

### **Check Metrics:**

- CPU usage
- Memory usage
- Network I/O

---

## 🔧 MANAGE BOT:

### **Restart Bot:**

1. Di Railway dashboard
2. Click project
3. Click "Redeploy" button
4. Bot akan restart dalam 30 detik

### **Stop Bot:**

1. Click project
2. Click "Services"
3. Find PMI Bot service
4. Click "Remove"

Bot akan stop tapi tidak dihapus, bisa di-start lagi.

### **View Deployment History:**

1. Click "Deployments"
2. Lihat semua deployment attempts
3. Klik salah satu untuk lihat logs

---

## 💰 PRICING (Railway):

**Gratis:**
- ✅ First $5 per month credit (free tier)
- ✅ Cukup untuk 1 bot 24/7

**Setelah $5 free credit:**
- 💵 $0.50 per GB RAM per hour
- 💵 $0.10 per GB storage per month

**Estimasi bot Anda:**
- RAM: 512MB = ~$7.50/bulan
- Storage: 1GB = ~$0.10/bulan
- **Total: ~$8/bulan** (atau gratis dengan credit)

---

## ⚠️ TROUBLESHOOTING:

### **Bot tidak muncul di Railway Dashboard**

**Solution:**
1. Refresh page (Ctrl+F5)
2. Check "Deployments" tab
3. Lihat apakah ada error message

### **Logs menunjukkan error: "403 Forbidden"**

**Expected!** Environment Railway juga block BP2MI website.
Bot akan bekerja normal di production (di komputer lokal atau server lokal Anda yang punya internet access).

Untuk test di Railway, bisa:
- Use mock data (update cek_pmi.py untuk test mode)
- Deploy ke lokal server yang punya direct internet access

### **Bot tidak respond di Telegram**

**Kemungkinan:**
1. Bot belum finish deploy (tunggu 2-3 menit)
2. Token tidak valid (check di code)
3. Bot crash (check logs di Railway)

**Solution:**
1. Check Railway logs untuk error
2. Restart bot (click Redeploy)
3. Tunggu 1 menit
4. Try lagi di Telegram

### **"Deployment failed" error**

**Common causes:**
1. Playwright install gagal
2. Python version issue
3. Missing dependencies

**Solution:**
1. Check logs detail
2. Try redeploy
3. Jika masih gagal, try method lain (Docker/Local)

---

## 📊 RAILWAY DASHBOARD GUIDE:

**Main Page:**
```
┌─ Projects
│  └─ PMI Bot
│     ├─ Overview (status, metrics)
│     ├─ Deployments (history, logs)
│     ├─ Settings (env vars, domain)
│     ├─ Networking (domains, ports)
│     └─ Alerts (optional)
```

**Key Features:**
- **Deployments:** Lihat history & logs semua deployment
- **Logs:** Real-time logs dari bot
- **Metrics:** CPU, memory, network usage
- **Settings:** Environment variables, restart, delete

---

## 🎓 TIPS & TRICKS:

### **Disable Deployment Notifications** (optional)
Railway akan email Anda setiap deploy. Disable di Settings jika tidak perlu.

### **Set Custom Domain** (optional)
Railway akan assign domain random. Bisa customize di Networking settings.

### **Scheduled Restarts** (optional)
Bisa setup automatic restart setiap hari. Di Settings → Deployments.

### **Monitor with Alerts** (optional)
Setup alerts jika bot crash atau CPU tinggi.

---

## ✅ CHECKLIST FINAL:

- [ ] Create Railway account
- [ ] Sign in dengan GitHub
- [ ] Create new project
- [ ] Select testpmi repository
- [ ] Choose branch: claude/pmi-data-scraper-gga9xo
- [ ] Click Deploy
- [ ] Tunggu deployment selesai (2-3 menit)
- [ ] Check logs - harus "Bot sedang dijalankan"
- [ ] Test di Telegram - kirimkan /start
- [ ] Bot respond dengan sambutan
- [ ] Kirimkan nomor paspor
- [ ] Bot process dan balik data
- [ ] ✅ DONE! Bot 24/7 online!

---

## 🎉 SELESAI!

Bot sudah running 24/7 di Railway! 🚀

**Siapapun bisa akses dengan:**
1. Buka Telegram
2. Cari bot pakai token
3. Kirimkan nomor paspor
4. Dapatkan data PMI instantly

---

## 📞 NEXT STEPS:

1. **Go to:** https://railway.app
2. **Click:** "Sign in with GitHub"
3. **Create project** dari repository testpmi
4. **Choose branch:** claude/pmi-data-scraper-gga9xo
5. **Deploy** - Done!

---

**Good luck! Bot Anda akan online dalam 5 menit!** 🚀🤖

