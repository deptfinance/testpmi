# 🔧 TROUBLESHOOTING - Bot Tidak Berjalan

Bot tidak berjalan? Mari kita debug step-by-step!

---

## ❓ STEP 1: DIMANA ERRORNYA?

### **Check 1: Di mana Anda mencoba deploy?**

- [ ] Railway.app
- [ ] Docker Compose (lokal)
- [ ] Local Python (komputer)
- [ ] Windows Task Scheduler
- [ ] Linux Systemd

---

## 🔍 STEP 2: LIHAT ERROR MESSAGE

### **Jika pakai Railway:**

1. **Buka** https://railway.app
2. **Login** dengan GitHub
3. **Klik project** "pmi-bot"
4. **Lihat "Deployments"** tab
5. **Lihat logs** - Ada error apa?

### **Jika pakai Docker Compose (lokal):**

```bash
docker-compose logs -f pmi-bot
```

Lihat error message-nya.

### **Jika pakai Local Python:**

```bash
python3 bot_pmi.py
```

Lihat error di console.

### **Jika pakai Systemd:**

```bash
sudo journalctl -u bot-pmi.service -n 50 -f
```

---

## 🆘 COMMON ERRORS & SOLUTIONS:

### **ERROR 1: "ModuleNotFoundError: No module named 'playwright'"**

**Cause:** Playwright not installed

**Fix:**
```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

---

### **ERROR 2: "Chromium not found"**

**Cause:** Chromium browser tidak installed

**Fix:**
```bash
python3 -m playwright install chromium
```

---

### **ERROR 3: "Invalid token" atau "401 Unauthorized"**

**Cause:** Token Telegram invalid atau expired

**Fix:**
1. Buka Telegram → @BotFather
2. Buat bot baru: `/newbot`
3. Copy token yang baru
4. Update di `bot_pmi.py` atau `docker-compose.yml`
5. Restart bot

---

### **ERROR 4: "Connection refused" atau "Network error"**

**Cause:** Internet connection problem atau proxy blocking

**Fix:**
1. Check internet connection: `ping google.com`
2. Check firewall settings
3. Try restart bot
4. Check jika ada proxy di network

---

### **ERROR 5: Deployment failed di Railway**

**Check logs untuk detail error:**

1. Buka Railway dashboard
2. Lihat "Deployments" → "View Logs"
3. Scroll up untuk lihat full error

**Common causes:**

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Dependencies tidak terinstall |
| `out of memory` | Bot running terlalu lama, restart |
| `build timeout` | Railway timeout, coba redeploy |
| `Dockerfile error` | Check syntax Dockerfile |

---

### **ERROR 6: Bot tidak respond di Telegram**

**Kemungkinan:**

1. **Bot belum selesai deploy** → Tunggu 2-3 menit
2. **Token wrong** → Check di code/env var
3. **Bot crashed** → Check logs
4. **Network issue** → Check connection

**Debug:**

```bash
# Check apakah bot running
ps aux | grep bot_pmi.py

# Check logs
sudo journalctl -u bot-pmi.service -f

# Restart bot
sudo systemctl restart bot-pmi.service
```

---

### **ERROR 7: "ProxyError" atau network blocked**

**Cause:** Proxy/firewall blocking Telegram API atau BP2MI

**Fix:**
- Check internet provider blocking
- Try dengan VPN
- Try dari network lain
- Contact ISP jika blocked

---

### **ERROR 8: Bot crash setelah beberapa menit**

**Cause:** Memory leak atau timeout issue

**Fix:**
1. Check logs untuk error
2. Restart bot
3. Check system resources (RAM, CPU)
4. Upgrade resources jika perlu

---

## 🔧 DIAGNOSTIC COMMANDS:

### **Check Bot Process:**

```bash
# Linux/Mac
ps aux | grep bot_pmi
ps aux | grep python3

# Windows (Command Prompt)
tasklist | find "python"
```

### **Check Network:**

```bash
# Test Telegram API access
curl -v https://api.telegram.org

# Test BP2MI access
curl -v https://siskop2mi.bp2mi.go.id

# Check DNS
nslookup api.telegram.org
```

### **Check Logs:**

```bash
# Last 50 lines
tail -50 bot.log

# Follow logs in real time
tail -f bot.log

# Count errors
grep -i error bot.log | wc -l
```

### **Check Resources:**

```bash
# Memory usage
free -h

# CPU usage
top -bn1 | head -20

# Disk space
df -h

# Docker container stats
docker stats pmi-bot
```

---

## 📋 DEPLOYMENT CHECKLIST:

- [ ] Python 3.7+ installed? → `python3 --version`
- [ ] pip installed? → `pip3 --version`
- [ ] dependencies installed? → `pip3 install -r requirements.txt`
- [ ] Chromium installed? → `python3 -m playwright install chromium`
- [ ] Token valid? → Check di @BotFather
- [ ] Internet working? → `ping google.com`
- [ ] Firewall allowing? → Check firewall settings
- [ ] Bot script existing? → `ls -la bot_pmi.py`

---

## 🚨 TIDAK ADA ERROR TAPI BOT TIDAK RESPOND:

**Kemungkinan:**

1. **Bot polling belum start** - Tunggu 30 detik
2. **Bot stuck di startup** - Cek logs
3. **Token not working** - Verify di BotFather
4. **Timeout too short** - Increase timeout di code

**Test manual:**

```python
# Test bot response manually
python3 << 'EOF'
import asyncio
from bot_pmi import bot_pmi, cek_pmi

# Test cek_pmi function
hasil = asyncio.run(cek_pmi("AU610053"))
print(f"Result: {hasil}")
EOF
```

---

## 📞 GETTING HELP:

**Provide these info:**

1. **Where deployed?** (Railway/Docker/Local/etc)
2. **Full error message** (copy-paste dari logs)
3. **Steps to reproduce** (apa yang Anda lakukan)
4. **Expected behavior** (apa yang harusnya terjadi)
5. **Actual behavior** (apa yang terjadi)

---

## 🎯 QUICK FIX CHECKLIST:

- [ ] Restart bot? → `python3 bot_pmi.py`
- [ ] Check logs? → See above
- [ ] Reinstall dependencies? → `pip3 install -r requirements.txt`
- [ ] Check token valid? → Test di BotFather
- [ ] Check internet? → `ping google.com`
- [ ] Check firewall? → Allow Telegram API
- [ ] Try different network? → Test dengan WiFi/4G lain

---

## 🆘 MASIH TIDAK BERHASIL?

**Coba ini:**

1. **Baca RAILWAY_SETUP.md** - Detail guide Railway
2. **Baca START_HERE.md** - Overview semua methods
3. **Check GitHub issues** - Mungkin ada yang pernah alami
4. **Contact support** - Railway/Docker/provider support

---

## 💡 TIPS:

1. **Check logs first** - 80% error terlihat di logs
2. **Restart bot** - Often fixes temporary issues
3. **Check token** - Token is critical
4. **Check network** - Most issues are network-related
5. **Use test mode** - Test logic tanpa network access

---

**Still stuck? Provide error message dan saya bantu debug!** 🚀
