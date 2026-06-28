"""
Bot Telegram untuk Cek Status PMI via BP2MI
Render.com deployment
"""

import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from cek_pmi import cek_pmi, cek_pmi_batch

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw")

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
        "Contoh: AU610053 atau E8531198\n\n"
        "Waktu proses: 10-20 detik"
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
        await update.message.reply_text("❌ Nomor paspor tidak valid (minimal 2 karakter)")
        return

    # Loading message
    msg = await update.message.reply_text(f"⏳ Mengecek: {paspor}...")

    try:
        # Cek data PMI
        data = await cek_pmi(paspor)

        if data and 'Status' not in data:
            # Format hasil
            result_msg = f"✅ *Data PMI Ditemukan*\n\n"
            for key, value in data.items():
                result_msg += f"*{key}*\n{value}\n\n"
            result_msg = result_msg.strip()

            await msg.delete()
            await update.message.reply_text(result_msg, parse_mode='Markdown')
        else:
            status = data.get('Status', 'Unknown') if data else 'No response'
            await msg.delete()
            await update.message.reply_text(
                f"❌ {paspor}\n{status}",
                parse_mode='Markdown'
            )

    except Exception as e:
        await msg.delete()
        await update.message.reply_text(
            f"❌ Error: `{str(e)[:100]}`",
            parse_mode='Markdown'
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages (auto-detect passport numbers)"""
    text = update.message.text.strip()

    # Jika terlihat seperti nomor paspor (alphanumeric, 2+ chars)
    if len(text) >= 2 and text.replace(" ", "").isalnum() and not text.startswith('/'):
        await cek_handler(update, context)
    else:
        await update.message.reply_text(
            "Kirimkan nomor paspor untuk dicek!\n\n"
            "Contoh: AU610053\n\n"
            "Atau gunakan: /cek AU610053"
        )

def main():
    """Start bot dengan polling"""
    print("=" * 60)
    print("🤖 BOT CECK PMI - TELEGRAM")
    print("=" * 60)
    print(f"\n✓ Token: {TELEGRAM_TOKEN[:30]}...")
    print("✓ Mode: Polling")
    print("\nBot siap menerima pesan dari Telegram...\n")

    try:
        # Create bot application
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("cek", cek_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

        # Start bot dengan polling
        print("Starting polling...\n")
        application.run_polling(allowed_updates=["message", "callback_query"])

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise

if __name__ == '__main__':
    main()
