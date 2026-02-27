import json
from datetime import datetime

TRADE_FILE = r"C:\policy_tool\Train\bnDemo\trade_history.json"

def load_trade_data(file_path=TRADE_FILE):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"transactions": []}


def count_today_trades(file_path=TRADE_FILE):
    data = load_trade_data(file_path)
    today = datetime.now().date()

    count = sum(
        1 for tx in data.get("transactions", [])
        if datetime.fromisoformat(tx["timestamp"]).date() == today
    )

    return f"{count} lần swap hôm nay"


def summarize_today_trades(file_path=TRADE_FILE):
    data = load_trade_data(file_path)
    today = datetime.now().date()

    trades = [
        tx for tx in data.get("transactions", [])
        if datetime.fromisoformat(tx["timestamp"]).date() == today
    ]

    if not trades:
        return {
            "total_trades": 0,
            "total_profit_percent": 0.0,
            "initial_coin": data.get("initial_coin", "N/A"),
        }

    total_profit = sum(tx.get("profit_percent", 0) for tx in trades)

    return {
        "total_trades": len(trades),
        "total_profit_percent": round(total_profit, 4),
        "initial_coin": data.get("initial_coin", "N/A"),
        "last_updated": data.get("last_updated", "N/A"),
    }


def get_wallet_status(file_path=TRADE_FILE):
    data = load_trade_data(file_path)

    transactions = data.get("transactions", [])
    initial_coin = data.get("initial_coin", "N/A")
    initial_amount = data.get("initial_amount", 0)

    if not transactions:
        return {
            "coin": initial_coin,
            "amount": initial_amount,
            "last_updated": "Chưa có giao dịch",
        }

    last_tx = transactions[-1]
    current_coin = last_tx["to_coin"]
    current_amount = last_tx["to_amount"]
    current_price_usdt = last_tx["prices"].get(f"{current_coin}/USDT", None)
    current_value_usdt = round(current_amount * current_price_usdt, 2) if current_price_usdt else None

    return {
        "coin": current_coin,
        "amount": round(current_amount, 6),
        "value_usdt": current_value_usdt,
        "last_updated": data.get("last_updated", "N/A"),
    }