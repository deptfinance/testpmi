"""
Bot Telegram untuk Cek Status PMI via BP2MI
Render.com deployment
"""

import asyncio
import logging
import os
import sys
import threading
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from cek_pmi import cek_pmi, cek_pmi_batch

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8829845272:AAFIr5llsLgyxSVsW-0T3E_rBT1kjpZcRLw")
PORT = int(os.environ.get("PORT", 10000))


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"PMI Bot is running")

    def log_message(self, format, *args):
        pass


def start_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    log.info("Health server listening on port %s", PORT)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selamat datang di Bot Cek PMI!\n\n"
        "Cara pakai:\n"
        "/cek [nomor_paspor]\n\n"
        "Contoh:\n"
        "/cek AU610053\n\n"
        "Bot akan otomatis cek data Anda ke BP2MI dan menampilkan hasilnya."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bantuan\n\n"
        "Commands:\n"
        "/start - Tampilkan pesan sambutan\n"
        "/help - Tampilkan bantuan ini\n"
        "/cek [nomor] - Cek data PMI\n\n"
        "Format nomor paspor:\n"
        "Contoh: AU610053 atau E8531198\n\n"
        "Waktu proses: 10-20 detik"
    )


async def cek_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "Masukkan nomor paspor\n\n"
            "Format: /cek [nomor_paspor]\n"
            "Contoh: /cek AU610053"
        )
        return

    paspor = context.args[0].strip()

    if len(paspor) < 2:
        await update.message.reply_text("Nomor paspor tidak valid (minimal 2 karakter)")
        return

    msg = await update.message.reply_text(f"Mengecek: {paspor}...")

    try:
        log.info("Checking passport: %s", paspor)
        data = await cek_pmi(paspor)
        log.info("Result for %s: %s", paspor, data)

        if data and 'Status' not in data:
            result_msg = "Data PMI Ditemukan\n\n"
            for key, value in data.items():
                result_msg += f"{key}: {value}\n"
            result_msg = result_msg.strip()

            await msg.delete()
            await update.message.reply_text(result_msg)
        else:
            status = data.get('Status', 'Unknown') if data else 'No response'
            await msg.delete()
            await update.message.reply_text(f"{paspor}: {status}")

    except Exception as e:
        log.error("Error checking %s: %s", paspor, traceback.format_exc())
        await msg.delete()
        await update.message.reply_text(f"Error: {str(e)[:200]}")


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if len(text) >= 2 and text.replace(" ", "").isalnum() and not text.startswith('/'):
        context.args = [text]
        await cek_handler(update, context)
    else:
        await update.message.reply_text(
            "Kirimkan nomor paspor untuk dicek!\n\n"
            "Contoh: AU610053\n\n"
            "Atau gunakan: /cek AU610053"
        )


async def _drop_webhook(application):
    try:
        await application.bot.delete_webhook(drop_pending_updates=True)
        log.info("Webhook deleted, polling ready")
    except Exception as e:
        log.warning("Failed to delete webhook: %s", e)


async def _post_init(application):
    await _drop_webhook(application)
    me = await application.bot.get_me()
    log.info("Bot connected: @%s (id=%s)", me.username, me.id)


def main():
    log.info("=" * 50)
    log.info("BOT CEK PMI - TELEGRAM")
    log.info("=" * 50)
    log.info("Token: %s...", TELEGRAM_TOKEN[:20])
    log.info("Port: %s", PORT)

    threading.Thread(target=start_health_server, daemon=True).start()

    try:
        application = Application.builder().token(TELEGRAM_TOKEN).post_init(_post_init).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("cek", cek_handler))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

        log.info("Starting polling...")
        application.run_polling(
            allowed_updates=["message", "callback_query"],
            drop_pending_updates=True,
        )

    except Exception as e:
        log.error("FATAL: %s", traceback.format_exc())
        raise


if __name__ == '__main__':
    main()
