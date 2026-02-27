import json
from datetime import datetime

TRADE_FILE = r"C:\policy_tool\Train\bnDemo\trade_history.json"

def inject_new_trade():
    with open(TRADE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    last_tx = data["transactions"][-1]
    new_swap_id = last_tx["swap_id"] + 1

    new_tx = {
        "timestamp": datetime.now().isoformat(),
        "swap_id": new_swap_id,
        "from_coin": last_tx["to_coin"],
        "to_coin": last_tx["from_coin"],
        "from_amount": last_tx["to_amount"],
        "to_amount": round(last_tx["to_amount"] * 1.018, 6),
        "profit_percent": round(1.8, 4),
        "prices": last_tx["prices"]
    }

    data["transactions"].append(new_tx)
    data["last_updated"] = new_tx["timestamp"]

    with open(TRADE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Injected swap_id={new_swap_id}: {new_tx['from_coin']} → {new_tx['to_coin']}")

if __name__ == "__main__":
    inject_new_trade()