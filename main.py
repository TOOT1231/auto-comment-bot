import requests, base64, json, time, os

email = os.getenv("123456789xdf3@gmail.com")
password = os.getenv("Gehrman3mk")
comment_text = os.getenv("Test2", "Auto comment")
anime_id = os.getenv("ANIME_ID", "532")
interval = 60 / float(os.getenv("CPM", "60"))

headers = {
    "User-Agent": "...",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://ios.sanime.net",
    "Referer": "https://ios.sanime.net/",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept-Language": "ar"
}

url = "https://app.sanime.net/function/h10.php?page=addcmd"

while True:
    item = {"post": comment_text, "id": anime_id, "fire": False}
    payload = {
        "email": email,
        "password": password,
        "item": base64.b64encode(json.dumps(item).encode()).decode()
    }
    resp = requests.post(url, data=payload, headers=headers)
    print(resp.text)
    time.sleep(interval)
