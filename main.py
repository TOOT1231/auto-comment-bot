import requests, base64, json, time

# بيانات الدخول والتعليق
email = "123456789xdf3@gmail.com"
password = "Gehrman3mk"
comment_text = "!!"
anime_id = "532"  # رقم المادة
cpm = 120  # عدد التعليقات في الدقيقة (مثلاً 60/30 = تعليق كل ثانيتين)

interval = 60 / cpm
count = 0  # عداد التعليقات

# إعداد headers مثل التطبيق تماماً
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

# رابط الإرسال
url = "https://app.sanime.net/function/h10.php?page=addcmd"

# التكرار اللانهائي
while True:
    try:
        # تجهيز البيانات
        item = {"post": comment_text, "id": anime_id, "fire": False}
        payload = {
            "email": email,
            "password": password,
            "item": base64.b64encode(json.dumps(item).encode()).decode()
        }

        # إرسال الطلب
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            count += 1
            if count % 10 == 0:
                print(f"✅ تم إرسال {count} تعليق")
        else:
            print(f"❌ فشل الإرسال. الحالة: {response.status_code}")

    except Exception as e:
        print(f"⚠️ خطأ: {e}")

    time.sleep(interval)
