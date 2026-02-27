from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from intent.router import route_message
from services.trade_watcher import watch_new_trades

BOT_TOKEN = "8584247201:AAGfYM_cHw0gYKSV5xW9hNpCT5dA9HOKjwI"
OWNER_CHAT_ID = "1343641388"  # ← thay bằng chat_id của bạn


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = str(update.effective_user.id)

    print(f"[DEBUG] chat_id = {update.effective_chat.id}")  # ← xem trong terminal

    response = route_message(user_id, user_text)
    await update.message.reply_text(response)


async def on_startup(app):
    print("[Bot] Khởi động watcher...")
    app.create_task(watch_new_trades(app.bot, OWNER_CHAT_ID, interval=10))


def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()