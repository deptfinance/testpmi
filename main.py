"""
Bot Telegram untuk Cek Status PMI via BP2MI
Render.com deployment
"""

import asyncio
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from cek_pmi import cek_pmi, cek_pmi_batch

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw")
PORT = int(os.environ.get("PORT", 10000))


class HealthHandler(BaseHTTPRequestHandler):
    """Minimal HTTP server so Render Web Service stays healthy.
    Render requires a process bound to $PORT; the polling bot itself
    does not open a port, so without this the service is killed."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"PMI Bot is running")

    def log_message(self, format, *args):
        pass  # silence access logs


def start_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    print(f"✓ Health server listening on port {PORT}")
    server.serve_forever()

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

async def _drop_webhook(application):
    """Delete any registered webhook so polling (getUpdates) can work.
    A lingering webhook causes Telegram to reject polling with 409 Conflict."""
    try:
        await application.bot.delete_webhook(drop_pending_updates=True)
        print("✓ Webhook dihapus (polling siap)")
    except Exception as e:
        print(f"⚠️ Gagal hapus webhook: {e}")


def main():
    """Start bot dengan polling"""
    print("=" * 60)
    print("🤖 BOT CECK PMI - TELEGRAM")
    print("=" * 60)
    print(f"\n✓ Token: {TELEGRAM_TOKEN[:30]}...")
    print("✓ Mode: Polling")
    print("\nBot siap menerima pesan dari Telegram...\n")

    # Start health-check HTTP server in background thread (for Render port binding)
    threading.Thread(target=start_health_server, daemon=True).start()

    try:
        # Create bot application
        application = Application.builder().token(TELEGRAM_TOKEN).post_init(_drop_webhook).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("cek", cek_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

        # Start bot dengan polling
        print("Starting polling...\n")
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True,
        )

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise

if __name__ == '__main__':
    main()
