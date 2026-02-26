from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from intent.router import route_message

BOT_TOKEN = "8584247201:AAGfYM_cHw0gYKSV5xW9hNpCT5dA9HOKjwI"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = str(update.effective_user.id)

    response = route_message(user_id, user_text)

    await update.message.reply_text(response)

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()