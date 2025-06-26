from flask import Flask
import threading
import requests, base64, json, time
from concurrent.futures import ThreadPoolExecutor

# إعداد Flask
app = Flask(__name__)

# إعداد بيانات التعليق
email = "123456789xdf3@gmail.com"
password = "Gehrman3mk"
comment_text = "؟.?"
anime_id = "532"

# إعدادات الإرسال
delay = 60 / 120  # كم ثانية بين كل دفعة كاملة
max_comments = None  # أقصى عدد تعليقات (أو None للانهائي)
parallel_comments = 30  # عدد التعليقات في نفس الوقت

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

def send_comment():
    try:
        item_data = {"post": comment_text, "id": anime_id, "fire": False}
        item_base64 = base64.b64encode(json.dumps(item_data).encode()).decode()
        payload = {"email": email, "password": password, "item": item_base64}
        url = "https://app.sanime.net/function/h10.php?page=addcmd"
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            print("✅ تم الإرسال!")
        else:
            print(f"❌ فشل: {response.status_code}")
    except Exception as e:
        print(f"❗ خطأ: {e}")

def send_comment_loop():
    sent_count = 0
    while True:
        if max_comments is not None and sent_count >= max_comments:
            print("🚫 تم الوصول للحد الأقصى من التعليقات.")
            break

        with ThreadPoolExecutor(max_workers=parallel_comments) as executor:
            for _ in range(parallel_comments):
                if max_comments is not None and sent_count >= max_comments:
                    break
                executor.submit(send_comment)
                sent_count += 1

        time.sleep(delay)

# لتشغيل الثريد مرة واحدة فقط
started = False

@app.before_request
def start_sending_once():
    global started
    if not started:
        started = True
        threading.Thread(target=send_comment_loop, daemon=True).start()

# واجهة بسيطة
@app.route('/')
def home():
    return "🤖 Auto Comment Bot is running with multi-threading!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
