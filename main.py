from flask import Flask
import threading
import requests, base64, json, time

# إعداد Flask
app = Flask(__name__)

# ====== الإعدادات ======
email = "123456789xdf3@gmail.com"
password = "Gehrman3mk"
comment_text = "TTT."
comment_per_minute = 10000  # كلما زادت القيمة زادت السرعة (مثال: 60 = كل ثانية، 120 = كل نصف ثانية)
max_parallel_comments = 10000  # التعليقات المتوازية في نفس اللحظة
delay = 60 / comment_per_minute  # لا تعدل هذا المتغير مباشرة

# ====== قائمة الأنميات ======
anime_targets = {
    "anime_532":     {"id": "532", "enabled": True},
    "anime_11708":   {"id": "11708", "enabled": True},
    "anime_11547":   {"id": "11547", "enabled": True},
    "anime_11707":   {"id": "11707", "enabled": True},
    "anime_11723":   {"id": "11723", "enabled": True},
    "anime_11706":   {"id": "11706", "enabled": True},
    "anime_11673":   {"id": "11673", "enabled": True},
    "anime_11704":   {"id": "11704", "enabled": True},
    "anime_11703":   {"id": "11703", "enabled": True},
    "anime_11702":   {"id": "11702", "enabled": True},
    "anime_11700":   {"id": "11700", "enabled": True},
    "anime_11705":   {"id": "11705", "enabled": True},
    "anime_11699":   {"id": "11699", "enabled": True},
    "anime_11698":   {"id": "11698", "enabled": True},
    "anime_11694":   {"id": "11694", "enabled": True},
    "anime_11697":   {"id": "11697", "enabled": True},
    "anime_11721":   {"id": "11721", "enabled": True},
    "anime_11718":   {"id": "11718", "enabled": True},
    "anime_11693":   {"id": "11693", "enabled": True},
    "anime_11692":   {"id": "11692", "enabled": True},
    "anime_11663":   {"id": "11663", "enabled": True},
    "anime_11710":   {"id": "11710", "enabled": True},
    "anime_11711":   {"id": "11711", "enabled": True},
    "anime_11691":   {"id": "11691", "enabled": True},
    "anime_11689":   {"id": "11689", "enabled": True},
    "anime_653":     {"id": "653",  "enabled": True},
    "anime_11686":   {"id": "11686", "enabled": True},
    "anime_11688":   {"id": "11688", "enabled": True},
    "anime_11684":   {"id": "11684", "enabled": True},
    "anime_11712":   {"id": "11712", "enabled": True}
}

# ====== رؤوس الطلب ======
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (SevenZero) (C38AGCA1-3F3F-401C-B9DD-DEC5055B86FC)",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://ios.sanime.net",
    "Referer": "https://ios.sanime.net/",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept-Language": "ar"
}

# ====== إرسال تعليق ======
def send_comment(anime_id):
    try:
        item_data = {"post": comment_text, "id": anime_id, "fire": False}
        item_base64 = base64.b64encode(json.dumps(item_data).encode()).decode()
        payload = {"email": email, "password": password, "item": item_base64}
        url = "https://app.sanime.net/function/h10.php?page=addcmd"
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            print(f"✅ تم إرسال التعليق إلى الانمي {anime_id}")
        else:
            print(f"❌ فشل الإرسال إلى الانمي {anime_id}، كود: {response.status_code}")
    except Exception as e:
        print(f"❗ خطأ أثناء الإرسال إلى {anime_id}: {e}")

# ====== حلقة الإرسال ======
def send_comment_loop():
    while True:
        enabled_animes = [anime["id"] for anime in anime_targets.values() if anime["enabled"]]
        for i in range(0, len(enabled_animes), max_parallel_comments):
            batch = enabled_animes[i:i + max_parallel_comments]
            threads = []
            for anime_id in batch:
                t = threading.Thread(target=send_comment, args=(anime_id,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        time.sleep(delay)

# ====== تشغيل السيرفر والخدمة ======
@app.route('/')
def home():
    return "🤖 Auto Comment Bot is running on Render!"

if __name__ == "__main__":
    threading.Thread(target=send_comment_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
