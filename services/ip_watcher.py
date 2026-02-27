import asyncio
import json
import requests
import config

CONFIG_FILE = config.CONFIG_FILE
IP_API = "https://api.ipify.org"


def load_last_ip():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("last_known_ip", "")
    except FileNotFoundError:
        return ""


def save_last_ip(ip: str):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = {}

    cfg["last_known_ip"] = ip

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def fetch_current_ip():
    try:
        r = requests.get(IP_API, timeout=5)
        return r.text.strip()
    except Exception as e:
        print(f"[IP Watcher] Lỗi fetch IP: {e}")
        return None


async def watch_ip_change(bot, chat_id, interval=60):
    last_ip = load_last_ip()
    print(f"[IP Watcher] Bắt đầu theo dõi, IP hiện tại: {last_ip or 'chưa có'}")

    while True:
        await asyncio.sleep(interval)

        current_ip = fetch_current_ip()
        if not current_ip:
            continue

        if last_ip == "":
            # Lần đầu chạy, lưu IP luôn
            save_last_ip(current_ip)
            last_ip = current_ip
            print(f"[IP Watcher] Lưu IP lần đầu: {current_ip}")
            continue

        if current_ip != last_ip:
            msg = (
                f"🌐 *IP thay đổi!*\n"
                f"📍 Cũ: `{last_ip}`\n"
                f"📍 Mới: `{current_ip}`"
            )
            await bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
            print(f"[IP Watcher] IP đổi: {last_ip} → {current_ip}")

            save_last_ip(current_ip)
            last_ip = current_ip