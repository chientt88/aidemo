from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from intent.router import route_message

BOT_TOKEN = ""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.
    user_id = str(update.effective_user.id)

    response = route_message(user_id, user_text)

    await update.message.reply_text(response)

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
