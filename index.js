const axios = require("axios");
const https = require("https");

const email = "123456789xdf3@gmail.com";
const password = "Gehrman3mk";
const commentText = "Test-3";
const commentsPerMinute = 60;

// قائمة الأنميات: فقط 532 مفعّل، والباقي غير مفعّل
const animeTargets = {
  532: true,
  11708: false,
  11547: false,
  11707: false,
  11723: false,
  11706: false,
  11673: false,
  11704: false,
  11703: false,
  11702: false,
  11700: false,
  11705: false,
  11699: false,
  11698: false,
  11694: false,
  11697: false,
  11721: false,
  11718: false,
  11693: false,
  11692: false,
  11663: false,
  11710: false,
  11711: false,
  11691: false,
  11689: false,
  653: false,
  11686: false,
  11688: false,
  11684: false,
  11712: false
};

const headers = {
  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (SevenZero)",
  "Content-Type": "application/x-www-form-urlencoded",
  "Origin": "https://ios.sanime.net",
  "Referer": "https://ios.sanime.net/",
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate, br",
  "Connection": "keep-alive",
  "Accept-Language": "ar"
};

const agent = new https.Agent({ keepAlive: true });

function sendComment(animeId) {
  const itemData = {
    post: commentText,
    id: animeId,
    fire: false
  };
  const itemBase64 = Buffer.from(JSON.stringify(itemData)).toString("base64");
  const payload = new URLSearchParams({
    email,
    password,
    item: itemBase64
  });

  return axios.post(
    "https://app.sanime.net/function/h10.php?page=addcmd",
    payload.toString(),
    { headers, httpsAgent: agent }
  );
}

function startCommenting() {
  const activeAnimeIds = Object.keys(animeTargets).filter(id => animeTargets[id]);

  console.log("🚀 بدأ الإرسال المستمر...");

  let counter = 0;

  setInterval(() => {
    counter++;
    activeAnimeIds.forEach(animeId => {
      sendComment(animeId)
        .then(() => console.log(`✅ [${animeId}] تعليق ${counter}`))
        .catch(err => console.error(`❌ [${animeId}] خطأ:`, err.message));
    });

    if (counter >= commentsPerMinute) counter = 0;
  }, 1000);
}

startCommenting();
