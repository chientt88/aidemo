from memory.database import init_db
from bot.tele_bot import start_bot

if __name__ == "__main__":
    init_db()
    start_bot()