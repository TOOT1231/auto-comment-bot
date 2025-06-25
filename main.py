import requests, base64, json, time

# 🟢 البيانات الأساسية مباشرة داخل الكود
email = "123456789xdf3@gmail.com"  # ✉️ إيميل الحساب
password = "Gehrman3mk"            # 🔒 كلمة المرور
comment_text = "Test2"          # 📝 نص التعليق
anime_id = "532"                   # 🔢 رقم المادة
cpm = 60                            # 🕒 عدد التعليقات في الدقيقة

# 🕰️ حساب الوقت بين كل تعليق (بالثواني)
interval = 60 / cpm

# 🧾 الهيدر مثل التطبيق بالضبط
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

# 🔁 حلقة إرسال التعليقات
url = "https://app.sanime.net/function/h10.php?page=addcmd"

while True:
    item = {"post": comment_text, "id": anime_id, "fire": False}
    payload = {
        "email": email,
        "password": password,
        "item": base64.b64encode(json.dumps(item).encode()).decode()
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        print("✅ تم إرسال التعليق:", response.text)
    else:
        print("❌ فشل الإرسال. الحالة:", response.status_code)

    time.sleep(interval)
