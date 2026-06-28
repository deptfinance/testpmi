# 📖 Panduan Instalasi & Penggunaan Script Cek PMI

## Prerequisites (Yang Diperlukan)

- Python 3.7 atau lebih baru
- pip (package manager Python)
- Internet connection
- Browser (Chromium akan diinstall otomatis)

---

## 🚀 Instalasi Step by Step

### **STEP 1: Install Python dan pip** 

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version  # Verifikasi
```

#### **Windows:**
1. Download dari: https://www.python.org/downloads/
2. Jalankan installer
3. ✅ **PENTING**: Centang "Add Python to PATH"
4. Klik "Install Now"
5. Buka Command Prompt (cmd) dan verifikasi:
   ```
   python --version
   pip --version
   ```

#### **Mac:**
```bash
# Jika pakai Homebrew:
brew install python3
python3 --version
```

---

### **STEP 2: Clone/Buka Repository**

Asumsikan file sudah ada di folder proyek Anda. Buka terminal/command prompt di folder tersebut.

```bash
cd /path/to/testpmi
```

---

### **STEP 3: Install Dependencies (Library yang Diperlukan)**

Jalankan command di bawah. Ini akan install Playwright dan dependencies lainnya:

#### **Linux/Mac:**
```bash
pip3 install -r requirements.txt
```

#### **Windows:**
```bash
pip install -r requirements.txt
```

**Output yang diharapkan:**
```
Successfully installed playwright-1.45.1
```

---

### **STEP 4: Install Chromium Browser**

Playwright memerlukan Chromium. Install dengan command:

#### **Linux/Mac:**
```bash
python3 -m playwright install chromium
```

#### **Windows:**
```bash
python -m playwright install chromium
```

**⏳ Ini mungkin butuh beberapa menit** (Chromium ukurannya ~200MB)

---

### **STEP 5: Verifikasi Instalasi**

Pastikan semuanya terinstall dengan benar:

#### **Linux/Mac:**
```bash
python3 -c "from playwright.async_api import async_playwright; print('✓ Playwright OK')"
```

#### **Windows:**
```bash
python -c "from playwright.async_api import async_playwright; print('✓ Playwright OK')"
```

**Jika output: `✓ Playwright OK` → Semuanya siap! ✓**

---

## 🎯 Cara Menggunakan Script

### **Format Dasar:**

#### **Linux/Mac:**
```bash
python3 cek_pmi.py <NOMOR_PASPOR>
```

#### **Windows:**
```bash
python cek_pmi.py <NOMOR_PASPOR>
```

### **Contoh Penggunaan:**

```bash
python3 cek_pmi.py AU610053
```

Atau dengan nomor paspor Anda sendiri:
```bash
python3 cek_pmi.py XX123456
```

### **Expected Output (Contoh):**

```
🔍 Mengecek data PMI untuk paspor: AU610053

📲 Membuka website BP2MI...
✓ Website terbuka

📖 Membaca captcha...
   Teks yang terlihat: 5 + 3
📝 Soal Captcha: 5 + 3
✓ Jawaban captcha: 8

✍️  Mengisi form...
   ✓ Nomor paspor: AU610053
   ✓ Jawaban captcha: 8

🔘 Mengklik tombol 'Cek Status'...
   ✓ Tombol diklik

⏳ Menunggu hasil...

============================================================
📊 HASIL PENCARIAN DATA PMI
============================================================
Nama                     : Budi Santoso
Negara Penempatan        : Arab Saudi
P3MI                     : PT Karya Bersama
Mitra LN                 : Al Rajhi
Alamat                   : Jl. Merdeka No. 42, Jakarta
Berlaku Hingga           : 2025-12-31
============================================================
```

---

## 🔧 Troubleshooting (Jika Ada Error)

### **Error 1: "command not found: python3"**
**Solusi:** Python tidak terinstall atau belum di PATH
- Install Python dulu (lihat STEP 1)
- Pada Windows, gunakan `python` bukan `python3`

### **Error 2: "ModuleNotFoundError: No module named 'playwright'"**
**Solusi:** Playwright belum diinstall
```bash
pip3 install playwright
```

### **Error 3: "Chromium not found"**
**Solusi:** Install Chromium browser
```bash
python3 -m playwright install chromium
```

### **Error 4: "Error: nomor paspor tidak diberikan"**
**Solusi:** Anda lupa menambahkan nomor paspor
```bash
# ❌ Salah
python3 cek_pmi.py

# ✓ Benar
python3 cek_pmi.py AU610053
```

### **Error 5: "Data tidak ditemukan di sistem BP2MI"**
**Solusi:** Nomor paspor tidak ada atau salah ketik
- Double check nomor paspor Anda
- Pastikan sudah benar (format, tanpa spasi)

### **Error 6: Script hang/stuck**
**Solusi:** Website mungkin slow
- Tunggu beberapa menit
- Jika tetap hang, tekan `Ctrl+C` dan coba lagi

---

## 📝 File Penjelasan

- **`requirements.txt`** - Daftar library Python yang dibutuhkan
- **`cek_pmi.py`** - Script utama untuk cek PMI
- **`SETUP.md`** - File ini (panduan instalasi)

---

## 💡 Tips

1. **Untuk batch processing** (mengecek banyak nomor), jalankan script berkali-kali:
   ```bash
   python3 cek_pmi.py AU610053
   python3 cek_pmi.py AU610054
   python3 cek_pmi.py AU610055
   ```

2. **Output screen besar?** Redirect ke file:
   ```bash
   python3 cek_pmi.py AU610053 > hasil.txt
   cat hasil.txt
   ```

3. **Jika butuh debug**, script sudah punya output yang jelas untuk setiap step

---

## ❓ Pertanyaan Umum

**Q: Apakah script ini menyimpan data?**
A: Tidak. Script hanya menampilkan hasil di screen. Data tidak disimpan.

**Q: Berapa lama script berjalan?**
A: Biasanya 5-10 detik (tergantung kecepatan internet)

**Q: Bisakah script ini gagal?**
A: Bisa, jika:
- Internet terputus
- Nomor paspor salah
- Website BP2MI down/error
- Captcha formula berubah (script perlu update)

**Q: Apakah aman?**
A: Ya, script hanya:
1. Membuka website resmi BP2MI
2. Membaca public information
3. Tidak menyimpan atau mengirim data ke tempat lain

---

## 🆘 Butuh Bantuan?

Jika ada error yang tidak dijelaskan di atas:
1. Salin full error message
2. Cek apakah ada typo di command
3. Pastikan file `cek_pmi.py` dan `requirements.txt` ada di folder yang sama
4. Coba jalankan ulang dari awal

Good luck! 🎉
