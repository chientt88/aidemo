from services.trade_analyzer import count_today_trades, get_wallet_status, summarize_today_trades

TOOLS = {
    "count_today_trades": {
        "description": "Đếm số lệnh Binance spot auto trade khớp hôm nay",
        "function": count_today_trades,
        "parameters": {}
    },
    "summarize_today_trades": {
        "description": "Tổng kết giao dịch hôm nay: số lần swap, tổng % lãi/lỗ, coin đang giữ",
        "function": summarize_today_trades,
        "parameters": {}
    },
    "get_wallet_status": {
        "description": "Xem ví hiện tại đang giữ coin gì, số lượng bao nhiêu và giá trị USDT",
        "function": get_wallet_status,
        "parameters": {}
    }
}