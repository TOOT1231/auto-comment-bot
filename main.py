from flask import Flask
import threading
import requests, base64, json, time

# إعداد Flask
app = Flask(__name__)

# إعداد بيانات التعليق
email = "123456789xdf3@gmail.com"
password = "Gehrman3mk"
comment_text = "صلوا على النبي"
anime_id = "532"
delay = 60 / 600  # كل دقيقة

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

def send_comment_loop():
    while True:
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
        time.sleep(delay)

# تشغيل الثريد عند تشغيل السيرفر
if __name__ == "__main__":
    threading.Thread(target=send_comment_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)

# عنوان واجهة بسيطة
@app.route('/')
def home():
    return "🤖 Auto Comment Bot is running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
