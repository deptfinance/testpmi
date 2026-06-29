#!/usr/bin/env python3
"""
Telegram Bot untuk Cek Data PMI (Pekerja Migran Indonesia)
Usage: python3 bot_pmi.py
Bot akan menunggu pesan dan cek data PMI berdasarkan nomor paspor yang dikirim user
"""

import asyncio
import logging
import os
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from cek_pmi import cek_pmi, display_results

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token Telegram Bot (from env var or hardcoded)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    welcome_message = f"""
👋 Halo {user.first_name}!

Selamat datang di **Bot Cek PMI (Pekerja Migran Indonesia)**

🎯 Cara menggunakan:
1. Kirimkan nomor paspor Anda (contoh: AU610053)
2. Bot akan otomatis mengecek data Anda di sistem BP2MI
3. Hasil akan ditampilkan dengan format yang rapi

📝 Contoh: Kirimkan pesan berisi nomor paspor seperti:
   AU610053

💡 Tips:
- Pastikan nomor paspor benar (tanpa spasi)
- Tunggu beberapa detik untuk hasil
- Bot akan memberikan data lengkap jika ditemukan

❓ Pertanyaan atau error? Coba lagi atau hubungi developer.

Silakan mulai dengan mengirim nomor paspor Anda! 🚀
"""
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
📖 **Panduan Penggunaan Bot PMI**

**1. Cara Cek Data:**
   Kirimkan nomor paspor Anda langsung
   Contoh: AU610053

**2. Data yang Akan Didapatkan:**
   ✓ Nama
   ✓ Negara Penempatan
   ✓ P3MI (Pemberi Kerja)
   ✓ Mitra LN
   ✓ Alamat
   ✓ Berlaku Hingga

**3. Format Nomor Paspor:**
   - Gunakan format standar (contoh: AU610053)
   - Jangan tambahkan spasi
   - Minimal 2 karakter

**4. Waktu Proses:**
   - Biasanya 5-10 detik per query
   - Tergantung kecepatan internet

**5. Jika Ada Error:**
   - Cek nomor paspor (benar/salah?)
   - Coba lagi dalam beberapa saat
   - Website BP2MI mungkin sedang maintenance

**Commands:**
/start - Tampilkan pesan sambutan
/help  - Tampilkan bantuan ini
/info  - Info tentang bot

Pertanyaan? Hubungi developer! 💬
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /info command"""
    info_text = """
ℹ️ **Info Bot PMI**

**Nama:** Bot Cek Data PMI
**Versi:** 1.0
**Developer:** Team PMI Checker

**Fitur:**
- ✓ Cek data PMI real-time
- ✓ Otomatis solving captcha
- ✓ Format output yang rapi
- ✓ Error handling yang baik
- ✓ Respons cepat

**Technology Stack:**
- Python 3.7+
- Playwright (web automation)
- Telegram Bot API
- Async/Await

**Source Code:**
https://github.com/deptfinance/testpmi

Terima kasih telah menggunakan bot ini! 🙏
"""
    await update.message.reply_text(info_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user message with passport number"""
    nomor_paspor = update.message.text.strip()

    # Validasi input
    if not nomor_paspor or len(nomor_paspor) < 2:
        await update.message.reply_text(
            "❌ Nomor paspor tidak valid\n\n"
            "Format yang benar:\n"
            "• Minimal 2 karakter\n"
            "• Tanpa spasi\n\n"
            "Contoh: AU610053\n\n"
            "Silakan coba lagi! 🔄"
        )
        return

    # Validasi format (hanya alphanumeric)
    if not nomor_paspor.replace(' ', '').isalnum():
        await update.message.reply_text(
            "❌ Format nomor paspor tidak valid\n\n"
            "Hanya gunakan huruf dan angka (tanpa simbol khusus)\n"
            "Contoh yang benar: AU610053\n\n"
            "Silakan coba lagi! 🔄"
        )
        return

    # Show loading message
    loading_msg = await update.message.reply_text(
        f"⏳ Sedang mengecek data PMI untuk paspor: **{nomor_paspor}**\n\n"
        "Proses ini mungkin membutuhkan waktu 5-10 detik...\n"
        "Mohon tunggu... 🔍",
        parse_mode='Markdown'
    )

    try:
        # Jalankan script cek PMI
        logger.info(f"Checking PMI for passport: {nomor_paspor}")
        hasil = await cek_pmi(nomor_paspor)

        # Format hasil
        if hasil:
            result_text = "✅ **DATA PMI DITEMUKAN**\n\n"
            result_text += "="*50 + "\n"

            # Mapping field names ke display names
            field_labels = {
                'nama': '👤 Nama',
                'negara_penempatan': '🌍 Negara Penempatan',
                'p3mi': '🏢 P3MI (Pemberi Kerja)',
                'mitra_ln': '🤝 Mitra LN',
                'alamat': '📍 Alamat',
                'berlaku_hingga': '📅 Berlaku Hingga',
            }

            for key, value in hasil.items():
                label = field_labels.get(key, key.replace('_', ' ').title())
                result_text += f"{label}\n{value}\n\n"

            result_text += "="*50 + "\n"
            result_text += "✅ Data berhasil diambil dari BP2MI"

        else:
            result_text = (
                "❌ **DATA TIDAK DITEMUKAN**\n\n"
                f"Nomor paspor **{nomor_paspor}** tidak ditemukan di sistem BP2MI.\n\n"
                "Kemungkinan:\n"
                "• Nomor paspor salah/typo\n"
                "• Data belum terdaftar di BP2MI\n"
                "• Website sedang maintenance\n\n"
                "Silakan cek kembali nomor paspor Anda! 🔄"
            )

        # Delete loading message dan send result
        await loading_msg.delete()
        await update.message.reply_text(result_text, parse_mode='Markdown')
        logger.info(f"Result sent for passport: {nomor_paspor}")

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error checking PMI: {error_msg}")

        try:
            await loading_msg.delete()
        except:
            pass

        # Provide helpful error message
        if "network" in error_msg.lower() or "connection" in error_msg.lower():
            response = (
                "⚠️ **Network Error**\n\n"
                "Tidak bisa akses website BP2MI.\n"
                "Kemungkinan:\n"
                "• Website sedang down\n"
                "• Internet connection error\n"
                "• Website sedang maintenance\n\n"
                "Silakan coba lagi dalam beberapa saat."
            )
        else:
            response = (
                "❌ **ERROR**\n\n"
                f"Error: `{error_msg[:80]}`\n\n"
                "Silakan coba lagi atau hubungi developer."
            )

        await update.message.reply_text(response, parse_mode='Markdown')


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and notify user"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


async def post_init(application: Application) -> None:
    """Set bot commands after initialization"""
    commands = [
        BotCommand("start", "Tampilkan pesan sambutan"),
        BotCommand("help", "Tampilkan panduan penggunaan"),
        BotCommand("info", "Info tentang bot"),
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    """Start the bot"""
    print("="*60)
    print("🤖 BOT CECK PMI - TELEGRAM")
    print("="*60)
    print(f"\n✓ Token: {TELEGRAM_BOT_TOKEN[:30]}..." if TELEGRAM_BOT_TOKEN else "❌ NO TOKEN SET")
    print("✓ Starting bot...")
    print("\nBot menunggu pesan dari user...\n")

    try:
        # Create the Application
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).post_init(post_init).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("info", info_command))

        # Message handler untuk nomor paspor
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Error handler
        application.add_error_handler(error_handler)

        # Start the Bot
        print("Press Ctrl+C to stop the bot\n")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        print(f"\n❌ ERROR STARTING BOT: {e}")
        print("\nTroubleshooting:")
        print("1. Check token is valid")
        print("2. Check internet connection")
        print("3. Try again in a few seconds")
        raise


if __name__ == '__main__':
    main()
