from telegram import Bot, Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from intent.router import route_message
from services.trade_watcher import watch_new_trades
from services.ip_watcher import watch_ip_change
from watcher.market_watcher import start_market_watcher
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = config.get("bot_token")
OWNER_CHAT_ID = config.get("owner_chat_id")

_bot_instance: Bot = None


def _send_notify(message: str):
    """Synchronous wrapper to send message via Telegram bot."""
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(_bot_instance.send_message(
                chat_id=OWNER_CHAT_ID,
                text=message,
                parse_mode="Markdown"
            ))
        else:
            loop.run_until_complete(_bot_instance.send_message(
                chat_id=OWNER_CHAT_ID,
                text=message,
                parse_mode="Markdown"
            ))
    except Exception as e:
        logger.error(f"Failed to send market notify: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = str(update.effective_user.id)

    print(f"[DEBUG] chat_id = {update.effective_chat.id}")

    response = route_message(user_id, user_text)
    await update.message.reply_text(response)


async def on_startup(app):
    print("[Bot] Khởi động watcher...")
    app.create_task(watch_new_trades(app.bot, OWNER_CHAT_ID, interval=10))
    app.create_task(watch_ip_change(app.bot, OWNER_CHAT_ID, interval=60))


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is running and monitoring market_status.json!")


def start_bot():
    global _bot_instance
    app = Application.builder().token(BOT_TOKEN).build()
    _bot_instance = app.bot

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    start_market_watcher(send_func=_send_notify)
    logger.info("Market watcher started.")

    app.run_polling()