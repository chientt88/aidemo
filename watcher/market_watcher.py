import json
import time
import threading
from pathlib import Path


MARKET_STATUS_FILE = "market_status.json"
POLL_INTERVAL = 5  # seconds


def format_market_message(record: dict) -> str:
    ts = record.get("timestamp", "N/A")
    holding = record.get("holding", {})
    equiv = record.get("equivalent", {})
    swap = record.get("if_swap_now", {})
    prices = record.get("prices", {})
    signal = record.get("signal_profit_percent", 0)

    coin = holding.get("coin", "?")
    amount = holding.get("amount", 0)
    price_usdt = holding.get("price_usdt", 0)
    value_usdt = holding.get("value_usdt", 0)

    to_coin = swap.get("to_coin", "?")
    receive = swap.get("receive_amount", 0)
    fee = swap.get("fee_deducted", "?")
    vs_baseline = swap.get("vs_baseline", 0)
    pnl_amount = swap.get("pnl_amount", 0)
    pnl_pct = swap.get("pnl_percent", 0)
    result = swap.get("result", "?")

    prices_str = "\n".join(f"  • {k}: {v}" for k, v in prices.items())

    message = (
        f"📊 *Market Status Update*\n"
        f"🕐 `{ts}`\n\n"
        f"💼 *Holding*\n"
        f"  Coin: `{coin}`\n"
        f"  Amount: `{amount:,.4f}`\n"
        f"  Price: `{price_usdt:,.6f} USDT`\n"
        f"  Value: `{value_usdt:,.4f} USDT`\n\n"
        f"💱 *Equivalent*\n"
        f"  SFP: `{equiv.get('sfp', 0):,.4f}`\n"
        f"  BNB: `{equiv.get('bnb', 0):,.6f}`\n"
        f"  USDT: `{equiv.get('usdt', 0):,.4f}`\n\n"
        f"💰 *Prices*\n{prices_str}\n\n"
        f"🔄 *If Swap Now → {to_coin}*\n"
        f"  Receive: `{receive:,.6f} {to_coin}`\n"
        f"  Fee: `{fee}`\n"
        f"  vs Baseline: `{vs_baseline:,.4f}`\n"
        f"  PnL: `{pnl_amount:,.6f}` (`{pnl_pct:.4f}%`)\n"
        f"  Result: {result}\n\n"
        f"📈 Signal Profit: `{signal:.4f}%`"
    )
    return message


def _load_records(filepath: Path) -> list:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def start_market_watcher(send_func, filepath: str = MARKET_STATUS_FILE, interval: int = POLL_INTERVAL):
    """
    Start a background watcher thread that monitors market_status.json.

    :param send_func: Async-compatible callable, signature: send_func(message: str)
    :param filepath: Path to the JSON file to monitor.
    :param interval: Polling interval in seconds.
    """
    path = Path(filepath)
    last_count = len(_load_records(path))

    def _watch():
        nonlocal last_count
        while True:
            time.sleep(interval)
            records = _load_records(path)
            current_count = len(records)
            if current_count > last_count:
                new_records = records[last_count:]
                for record in new_records:
                    msg = format_market_message(record)
                    send_func(msg)
                last_count = current_count

    thread = threading.Thread(target=_watch, daemon=True)
    thread.start()
    return thread