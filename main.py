from flask import Flask
import requests, base64, json, time
from concurrent.futures import ThreadPoolExecutor
import threading

app = Flask(__name__)

# إعداد البيانات
email = "123456789xdf3@gmail.com"
password = "Gehrman3mk"
comment_text = "TT"
delay = 60 / 240  # 60 تعليق في الدقيقة = 1 تعليق كل ثانية
max_comments = None  # لا نهائي
parallel_comments = 10  # عدد التعليقات المتزامنة

# تفعيل / تعطيل الأنميات
anime_targets = {
    "anime_532": True,
    "anime_11708": True,
    "anime_11547": True,
    "anime_11707": True,
    "anime_11723": True,
    "anime_11706": True,
    "anime_11673": True,
    "anime_11704": True,
    "anime_11703": True,
    "anime_11702": True,
    "anime_11700": True,
    "anime_11705": True,
    "anime_11699": True,
    "anime_11698": True,
    "anime_11694": True,
    "anime_11697": True,
    "anime_11721": True,
    "anime_11718": True,
    "anime_11693": True,
    "anime_11692": True,
    "anime_11663": True,
    "anime_11710": True,
    "anime_11711": True,
    "anime_11691": True,
    "anime_11689": True,
    "anime_653": True,
    "anime_11686": True,
    "anime_11688": True,
    "anime_11684": True,
    "anime_11712": True
}

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

def send_comment(anime_id):
    try:
        item_data = {"post": comment_text, "id": anime_id, "fire": False}
        item_base64 = base64.b64encode(json.dumps(item_data).encode()).decode()
        payload = {"email": email, "password": password, "item": item_base64}
        url = "https://app.sanime.net/function/h10.php?page=addcmd"
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            print(f"✅ تعليق أُرسل بنجاح إلى {anime_id}")
        else:
            print(f"❌ فشل في {anime_id}: {response.status_code}")
    except Exception as e:
        print(f"⚠️ خطأ في {anime_id}: {e}")

def start_comment_loop():
    count = 0
    active_ids = [aid.split("_")[1] for aid, active in anime_targets.items() if active]

    while True:
        with ThreadPoolExecutor(max_workers=parallel_comments) as executor:
            for anime_id in active_ids:
                executor.submit(send_comment, anime_id)

        count += 1
        if max_comments is not None and count >= max_comments:
            break
        time.sleep(delay)

@app.route("/")
def home():
    return "🤖 Auto Comment Bot is Running!"

# بدء المهمة في الخلفية عند تشغيل الخادم
if __name__ == "__main__":
    threading.Thread(target=start_comment_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
