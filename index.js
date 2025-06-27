const axios = require("axios");
const https = require("https");

const email = "123456789xdf3@gmail.com";
const password = "Gehrman3mk";
const commentText = "Zzz";

// عدد التعليقات لكل دقيقة لكل أنمي
const commentsPerMinute = 60;

// قائمة الأنميات
const animeTargets = {
  532: true,
  11708: true,
  11547: true,
  11707: true,
  11723: true,
  11706: true,
  11673: true,
  11704: true,
  11703: true,
  11702: true,
  11700: true,
  11705: true,
  11699: true,
  11698: true,
  11694: true,
  11697: true,
  11721: true,
  11718: true,
  11693: true,
  11692: true,
  11663: true,
  11710: true,
  11711: true,
  11691: true,
  11689: true,
  653: true,
  11686: true,
  11688: true,
  11684: true,
  11712: true
};

// إعداد headers
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

// تحسين الاتصال باستخدام https.Agent (Keep-Alive)
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

  // كل ثانية يتم إرسال تعليق لكل أنمي
  setInterval(() => {
    counter++;
    activeAnimeIds.forEach(animeId => {
      sendComment(animeId)
        .then(() => console.log(`✅ [${animeId}] تعليق ${counter}`))
        .catch(err => console.error(`❌ [${animeId}] خطأ:`, err.message));
    });

    if (counter >= commentsPerMinute) counter = 0;

  }, 1000); // كل ثانية
}

startCommenting();
