#!/usr/bin/env python3
"""
Script untuk mengecek data Pekerja Migran Indonesia (PMI) di BP2MI
Usage: python3 cek_pmi.py <NOMOR_PASPOR>
Contoh: python3 cek_pmi.py AU610053
"""

import sys
import re
import asyncio
from playwright.async_api import async_playwright


async def solve_captcha(captcha_text):
    """
    Memecahkan captcha matematika sederhana
    Contoh: "5 + 3" atau "8 - 2"
    """
    print(f"📝 Soal Captcha: {captcha_text}")

    try:
        # Pattern untuk operasi matematika: "angka operator angka"
        match = re.match(r'(\d+)\s*([\+\-\*/])\s*(\d+)', captcha_text)

        if not match:
            print("❌ Format captcha tidak dikenali")
            return None

        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))

        # Hitung hasil
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            result = int(num1 / num2)
        else:
            return None

        print(f"✓ Jawaban captcha: {result}")
        return str(result)

    except Exception as e:
        print(f"❌ Error memecahkan captcha: {e}")
        return None


async def extract_table_data(page):
    """
    Mengambil data hasil dari halaman
    """
    try:
        # Tunggu sampai tabel muncul (atau pesan tidak ditemukan)
        await page.wait_for_timeout(2000)

        # Cek apakah ada pesan error (PMI tidak ditemukan)
        error_elements = await page.query_selector_all('text="Data tidak ditemukan"')
        if error_elements:
            print("❌ Data PMI tidak ditemukan di sistem BP2MI")
            return None

        # Cari tabel hasil
        table_rows = await page.query_selector_all('table tr')

        if not table_rows:
            print("⚠️ Tabel hasil tidak ditemukan")
            return None

        data = {}

        # Parse setiap baris tabel
        for row in table_rows:
            cells = await row.query_selector_all('td')
            if len(cells) >= 2:
                label = await cells[0].inner_text()
                value = await cells[1].inner_text()
                # Simpan dengan label yang dibersihkan
                key = label.strip().rstrip(':').lower().replace(' ', '_')
                data[key] = value.strip()

        return data if data else None

    except Exception as e:
        print(f"⚠️ Error mengambil data: {e}")
        return None


async def cek_pmi(nomor_paspor):
    """
    Fungsi utama untuk mengecek data PMI
    """
    print(f"\n🔍 Mengecek data PMI untuk paspor: {nomor_paspor}\n")

    async with async_playwright() as p:
        # Gunakan chromium yang sudah pre-installed di environment
        browser = await p.chromium.launch(
            headless=True
        )
        page = await browser.new_page()

        try:
            # Buka website
            print("📲 Membuka website BP2MI...")
            try:
                await page.goto("https://siskop2mi.bp2mi.go.id/publik/cek_status",
                              wait_until="domcontentloaded",
                              timeout=30000)
            except Exception as nav_error:
                print(f"⚠️  Warning navigasi: {nav_error}")
                print("   Lanjut dengan coba akses halaman...")
            print("✓ Website terbuka")

            # Ambil teks captcha
            print("\n📖 Membaca captcha...")
            captcha_element = await page.query_selector('label')
            if not captcha_element:
                print("❌ Captcha tidak ditemukan di halaman")
                await browser.close()
                return None

            captcha_text = await captcha_element.inner_text()
            print(f"   Teks yang terlihat: {captcha_text}")

            # Pecahkan captcha
            jawaban = await solve_captcha(captcha_text)
            if not jawaban:
                print("❌ Gagal memecahkan captcha")
                await browser.close()
                return None

            # Isi nomor paspor
            print("\n✍️  Mengisi form...")
            input_paspor = await page.query_selector('input[name="nomor_paspor"]')
            if input_paspor:
                await input_paspor.fill(nomor_paspor)
                print(f"   ✓ Nomor paspor: {nomor_paspor}")

            # Isi jawaban captcha
            input_captcha = await page.query_selector('input[name="jawaban_captcha"]')
            if input_captcha:
                await input_captcha.fill(jawaban)
                print(f"   ✓ Jawaban captcha: {jawaban}")

            # Klik tombol Cek Status
            print("\n🔘 Mengklik tombol 'Cek Status'...")
            button = await page.query_selector('button[type="submit"]')
            if button:
                await button.click()
                print("   ✓ Tombol diklik")

            # Ambil hasil
            print("\n⏳ Menunggu hasil...")
            hasil = await extract_table_data(page)

            return hasil

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

        finally:
            await browser.close()


def display_results(data):
    """
    Menampilkan hasil dengan format yang rapi
    """
    if not data:
        print("❌ Tidak ada data untuk ditampilkan\n")
        return

    print("\n" + "="*60)
    print("📊 HASIL PENCARIAN DATA PMI")
    print("="*60)

    # Mapping nama field ke label yang lebih user-friendly
    field_labels = {
        'nama': 'Nama',
        'negara_penempatan': 'Negara Penempatan',
        'p3mi': 'P3MI',
        'mitra_ln': 'Mitra LN',
        'alamat': 'Alamat',
        'berlaku_hingga': 'Berlaku Hingga',
        'paspor': 'Nomor Paspor',
        'status': 'Status'
    }

    for key, value in data.items():
        label = field_labels.get(key, key.replace('_', ' ').title())
        print(f"{label:<25}: {value}")

    print("="*60 + "\n")


async def main():
    """
    Fungsi main - entry point script
    """
    # Cek apakah nomor paspor diberikan sebagai argument
    if len(sys.argv) < 2:
        print("❌ Error: Nomor paspor tidak diberikan\n")
        print("Penggunaan: python3 cek_pmi.py <NOMOR_PASPOR>")
        print("Contoh: python3 cek_pmi.py AU610053\n")
        sys.exit(1)

    nomor_paspor = sys.argv[1]

    # Validasi format nomor paspor (minimal 5 karakter)
    if not nomor_paspor or len(nomor_paspor) < 2:
        print("❌ Nomor paspor tidak valid")
        sys.exit(1)

    # Jalankan proses cek PMI
    hasil = await cek_pmi(nomor_paspor)
    display_results(hasil)


if __name__ == "__main__":
    asyncio.run(main())
