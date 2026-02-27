from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from intent.router import route_message
from services.trade_watcher import watch_new_trades
from services.ip_watcher import watch_ip_change
import config

BOT_TOKEN = config.get("bot_token")
OWNER_CHAT_ID = config.get("owner_chat_id")


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


def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()