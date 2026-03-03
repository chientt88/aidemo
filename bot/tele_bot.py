from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from intent.router import route_message
from services.trade_watcher import watch_new_trades
from services.ip_watcher import watch_ip_change
from watcher.market_watcher import start_market_watcher
import asyncio
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = config.get("bot_token")
OWNER_CHAT_ID = config.get("owner_chat_id")

_bot_instance: Bot = None
_main_loop: asyncio.AbstractEventLoop = None


def _send_notify(message: str):
    """Thread-safe wrapper to send message from background watcher thread."""
    if _bot_instance is None or _main_loop is None:
        logger.warning("[MarketWatcher] Bot not ready yet, dropping message.")
        return
    try:
        future = asyncio.run_coroutine_threadsafe(
            _bot_instance.send_message(
                chat_id=OWNER_CHAT_ID,
                text=message,
                parse_mode="Markdown"
            ),
            _main_loop
        )
        # Optional: wait up to 10s and log if failed
        future.result(timeout=10)
    except Exception as e:
        logger.error(f"[MarketWatcher] Failed to send notify: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = str(update.effective_user.id)

    print(f"[DEBUG] chat_id = {update.effective_chat.id}")

    response = route_message(user_id, user_text)
    await update.message.reply_text(response)


async def on_startup(app):
    global _main_loop
    print("[Bot] Khởi động watcher...")
    # Capture the running loop AFTER run_polling() has started it
    _main_loop = asyncio.get_running_loop()
    app.create_task(watch_new_trades(app.bot, OWNER_CHAT_ID, interval=10))
    app.create_task(watch_ip_change(app.bot, OWNER_CHAT_ID, interval=60))
    # Start market watcher here so _main_loop is guaranteed to be running
    start_market_watcher(send_func=_send_notify)
    logger.info("[Bot] Market watcher started.")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is running and monitoring market_status.json!")


def start_bot():
    global _bot_instance
    app = Application.builder().token(BOT_TOKEN).post_init(on_startup).build()
    _bot_instance = app.bot

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()