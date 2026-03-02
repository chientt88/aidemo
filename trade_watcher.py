import json
import asyncio
import config


def load_last_swap_id():
    file_path = config.get("trade_history_file")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        transactions = data.get("transactions", [])
        if not transactions:
            return 0
        return transactions[-1]["swap_id"]
    except FileNotFoundError:
        return 0


async def watch_new_trades(bot, chat_id, interval=10):
    """
    Chạy background, cứ `interval` giây check 1 lần.
    Nếu có swap_id mới → gửi tin nhắn cho user.
    """
    file_path = config.get("trade_history_file")
    last_known_id = load_last_swap_id()
    print(f"[Watcher] Bắt đầu theo dõi, swap_id hiện tại: {last_known_id}")

    while True:
        await asyncio.sleep(interval)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            transactions = data.get("transactions", [])
            if not transactions:
                continue

            new_txs = [tx for tx in transactions if tx["swap_id"] > last_known_id]

            for tx in new_txs:
                msg = (
                    f"🔔 *Giao dịch mới!*\n"
                    f"🔄 {tx['from_coin']} → {tx['to_coin']}\n"
                    f"📦 {round(tx['from_amount'], 4)} → {round(tx['to_amount'], 4)}\n"
                    f"📈 Lãi: `{round(tx['profit_percent'], 4)}%`\n"
                    f"🕐 {tx['timestamp']}"
                )
                await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")

            if new_txs:
                last_known_id = new_txs[-1]["swap_id"]

        except Exception as e:
            print(f"[Watcher] Lỗi: {e}")