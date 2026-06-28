"""
Bot Telegram untuk Cek Status PMI via BP2MI
Deployment di Render.com
"""

import asyncio
import re
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from playwright.async_api import async_playwright

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw")
PORT = int(os.environ.get("PORT", 10000))


async def cek_pmi(paspor: str) -> dict:
    """Cek data PMI dari website BP2MI"""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            page = await browser.new_page()

            # Buka website
            await page.goto(
                "https://siskop2mi.bp2mi.go.id/publik/cek_status",
                timeout=30000,
                wait_until="domcontentloaded"
            )
            await page.wait_for_timeout(2000)

            # Isi nomor paspor
            try:
                await page.fill("input[name='t_paspor']", paspor)
            except:
                await page.fill("input[placeholder*='paspor']", paspor)

            # Baca captcha
            captcha_text = ""
            try:
                captcha_elem = await page.query_selector("#captcha")
                if captcha_elem:
                    captcha_text = await captcha_elem.text_content()
            except:
                try:
                    captcha_text = await page.locator("text=/\\d+\\s*[\\+\\-\\*]\\s*\\d+/").first.text_content()
                except:
                    pass

            # Hitung captcha
            if captcha_text:
                captcha_text = captcha_text.replace("×", "*").replace("x", "*").replace("X", "*")
                match = re.search(r'(\d+)\s*([\+\-\*])\s*(\d+)', captcha_text)
                if match:
                    a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
                    if op == '+':
                        result = a + b
                    elif op == '-':
                        result = a - b
                    else:
                        result = a * b

                    # Isi jawaban captcha
                    try:
                        await page.fill("input[name='t_captcha']", str(result))
                    except:
                        await page.fill("input[placeholder*='captcha']", str(result))

            # Klik tombol
            try:
                await page.click("button:has-text('Cek Status')")
            except:
                await page.click("button[type='submit']")

            await page.wait_for_timeout(3000)

            # Extract data
            try:
                data = await page.evaluate("""() => {
                    const rows = document.querySelectorAll('table.table tr');
                    const result = {};
                    rows.forEach(row => {
                        const cells = row.querySelectorAll('td');
                        if (cells.length >= 2) {
                            const label = cells[0].textContent.trim();
                            const value = cells[1].textContent.trim();
                            if (label && value) {
                                result[label] = value;
                            }
                        }
                    });
                    return result;
                }""")
            except:
                data = {}

            await browser.close()
            return data if data else None

    except Exception as e:
        print(f"Error: {e}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 Selamat datang di Bot Cek PMI!\n\n"
        "Cara pakai:\n"
        "/cek [nomor_paspor]\n\n"
        "Contoh:\n"
        "/cek AU610053\n\n"
        "Bot akan otomatis cek data Anda ke BP2MI dan menampilkan hasilnya."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        "📖 Bantuan\n\n"
        "Commands:\n"
        "/start - Tampilkan pesan sambutan\n"
        "/help - Tampilkan bantuan ini\n"
        "/cek [nomor] - Cek data PMI\n\n"
        "Format nomor paspor:\n"
        "Contoh: AU610053\n\n"
        "Waktu proses: 5-10 detik"
    )


async def cek_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cek command"""
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "❌ Masukkan nomor paspor\n\n"
            "Format: /cek [nomor_paspor]\n"
            "Contoh: /cek AU610053"
        )
        return

    paspor = context.args[0].strip()

    # Validasi
    if len(paspor) < 2:
        await update.message.reply_text(
            "❌ Nomor paspor tidak valid\n"
            "Minimal 2 karakter"
        )
        return

    # Loading message
    msg = await update.message.reply_text(f"⏳ Mengecek data PMI untuk paspor: `{paspor}`\n\nMohon tunggu...", parse_mode='Markdown')

    try:
        data = await cek_pmi(paspor)

        if data and len(data) > 0:
            # Format hasil
            result_msg = f"✅ *Data PMI Ditemukan*\n\n"
            result_msg += f"Paspor: `{paspor}`\n"
            result_msg += "─" * 40 + "\n"

            for key, value in data.items():
                result_msg += f"*{key}*\n{value}\n\n"

            result_msg += "─" * 40 + "\n"
            result_msg += "✅ Data berhasil diambil dari BP2MI"

            await msg.delete()
            await update.message.reply_text(result_msg, parse_mode='Markdown')
        else:
            await msg.delete()
            await update.message.reply_text(
                f"❌ Data tidak ditemukan untuk paspor `{paspor}`\n\n"
                "Kemungkinan:\n"
                "• Nomor paspor salah\n"
                "• Data belum terdaftar\n"
                "• Website sedang maintenance\n\n"
                "Coba lagi dengan nomor yang benar.",
                parse_mode='Markdown'
            )

    except Exception as e:
        await msg.delete()
        await update.message.reply_text(
            f"❌ Error: `{str(e)[:100]}`\n\n"
            "Silakan coba lagi dalam beberapa saat.",
            parse_mode='Markdown'
        )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    text = update.message.text.strip()

    # Jika terlihat seperti nomor paspor
    if len(text) >= 2 and text.replace(" ", "").isalnum():
        await cek_handler(update, context)
    else:
        await update.message.reply_text(
            "Kirimkan nomor paspor untuk dicek!\n\n"
            "Contoh: AU610053\n\n"
            "Atau gunakan command: /cek AU610053"
        )


def main():
    """Start bot dengan Telegram Bot API"""
    print("=" * 60)
    print("🤖 BOT CECK PMI - RENDER.COM")
    print("=" * 60)
    print(f"\n✓ Starting bot...")
    print(f"✓ Token: {TELEGRAM_TOKEN[:30]}...")
    print(f"✓ Mode: Webhook (PORT: {PORT})")
    print("\nBot siap menerima pesan dari Telegram...\n")

    try:
        # Create bot application
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("cek", cek_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

        # Start bot dengan polling (untuk development/testing)
        # Untuk production, gunakan webhook
        print("Starting polling...")
        application.run_polling(allowed_updates=["message", "callback_query"])

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == '__main__':
    main()
